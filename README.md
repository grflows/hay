# hay
a tiny compiler that only produces prints

requirements: gcc

Language:
// this is the entire language
print "whatever you want" // this is a comment

Usage:
python hay.py test.hay

## compiler overview
this readme explains how hay was written, and also gives a general idea about how transpilers/compilers/interpreters are written. Have a nice read :).

source -> lexer() -> \[tokens] -> parser() -> {ast} -> codegen() -> C code -> gcc -> .bin

### lexer
it's main job is to scan the source string and produce a list of identified tokens
print "hello word" // comment 
becomes:
\['PRNT', ('STR', 'hello world'), 'CMNT', 'NL']
it doesn't matter if a token is a string 'PRNT' or a const int like  PRNT (e.g. PRNT = 32).
What matters is tokenizing a long source code string into a list of tokens.
But why? Why can't we just source.split(" "), pattern match and execute (e.g if source\[i] == 'print': print(source[:i]))?
Try it! It becomes complex very quickly, but for a simple DSL, sure.
A lexer->parser->codegen pipe line helps with complexity, scale, and sanity. It's what pipe lines do.

#### how was the lexer build?
a lexer is basically a text scanner with pattern matching. Scan, and match. 

*SCAN:* For the scanning you can do it the standard way; one character at a time like hay does. Or you can split the source first and then iterate over each word (and why not, iterate over a whole line!).
The only constrains for a scanner is performance. Do you want to scan once and match? Do you want to scan for whiteSpace to split the source, and then scan each word a second time and then match? Whatever you fancy.
Scanning by character is pretty neat if i say so myself, here's why:

length = len(source)
while i < length:
  char = source[i]

  if 'a' < char < 'z':
    start = i
    while i < length and not source[i].isspace():
      i += 1
    word = source[start:i]
    match(word)

*MATCH:* Now this is where the magic is, and also the complexity of a lexer. As far as I know, and i know very little, there are two methods to match:

1\ directly compare. If n is number of keywords in your lang, it's O(n**C*). *C* depends on your optimization. There're two ways to implement this:
  - if word == KEYWORD: return token
  - Regex for the strong of hearts

2\ hashing aka let the table do the work. If n is number of keywords in your lang, it's O(1). This is how lexers for most of the languages you know and love handle matching. And there're two implementations:
  - *keyword table:* dictionary.get(word) // either gives corresponding token or None
  this is how small languages like Lua do it, hand written matching for each keyword.
  - *state transition table / DFA:* table(previous state, this char) -> next state.
  The goal is to reach a final state of {final_state: token, new_state} or syntax_error.
  For "print" we start from say table(new_state, p) -> p_state.
  Then table(p_state, r) -> r_state ... Finally reaching table(print_state, " ") -> \['PRNT', new_state] giving us the token.
  And the table looks like this:

  table = {
  ('new_state', 'p'): 'p_state',
  ('p_state', 'r'): 'pr_state',
  ('pr_state', 'i'): 'pri_state',
  # ... etc,
  ('print_state', ' '): ['PRNT', 'new_state']
  }
