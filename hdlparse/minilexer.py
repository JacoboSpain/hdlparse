# -*- coding: utf-8 -*-
# Copyright © 2017 Kevin Thibedeau
# Distributed under the terms of the MIT license
from __future__ import print_function

import re

'''Minimalistic lexer engine inspired by the PyPigments RegexLexer'''

__version__ = '1.0.7'

class MiniLexer(object):
  '''Simple lexer state machine with regex matching rules'''

  def __init__(self, tokens, flags=re.MULTILINE):
    '''Create a new lexer
    
    Args:
      tokens (dict(match rules)): Hierarchical dict of states with a list of regex patterns and transitions
      flags (int): Optional regex flags
    '''
    self.tokens = {}
    self.flags  = flags
    # Pre-process the state definitions
    for state, patterns in tokens.iteritems():
      full_patterns = []
      for p in patterns:
        pat = re.compile(p[0], flags)
        action = p[1]
        new_state = p[2] if len(p) >= 3 else None

        # Convert pops into an integer
        if new_state and new_state.startswith('#pop'):
          try:
            new_state = -int(new_state.split(':')[1])
          except IndexError, ValueError:
            new_state = -1

        full_patterns.append((pat, action, new_state))
      self.tokens[state] = full_patterns
      #print("[minilexer] [state = {}] type(state)={}".format(state,type(state)) )

      
  def insert_new_token(self,state,new_token):
  
      #print('[insert_new_token] longitud token[state]',len(self.tokens[state]))
      for patterns in new_token : #.iteritems():
        pat = re.compile(patterns[0], self.flags)
        action = patterns[1]
        self.tokens[state].append((pat,action,None))
      #print('[insert_new_token] longitud  FInal token[state]',len(self.tokens[state]))
      
  def delete_last_token(self,state):
    '''
        Elimina el ultimo elemento de la lista.
    '''
    self.tokens[state].pop()
    
    
    
    
  def run(self, text):
    '''Run lexer rules against a source text

    Args:
      text (str): Text to apply lexer to

    Yields:
      A sequence of lexer matches.
    '''

    stack = ['root']
    pos = 0

    self.patterns = self.tokens[stack[-1]]

    while True:
      for pat, action, new_state in self.patterns:
        #print("[minilexer] action = {}".format(action))
        
        m = pat.match(text, pos)
        if m:
          #print("[minilexer] se encontro {}".format(action))
          if action:
            #print('## MATCH: {} -> {}'.format(m.group(), action))
            yield (pos, m.end()-1), action, m.groups()
           
          pos = m.end()

          if new_state:
            if isinstance(new_state, int): # Pop states
              del stack[new_state:]
            else:
              stack.append(new_state)

            #print('## CHANGE STATE:', pos, new_state, stack)
            self.patterns = self.tokens[stack[-1]]

          break

      else:
        try:
          if text[pos] == '\n':
            pos += 1
            continue
          pos += 1
        except IndexError:
          break
  
