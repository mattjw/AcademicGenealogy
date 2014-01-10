# -*- coding: utf-8 -*-


#
#
# Colour scheme
#

COLOUR_MISSING_PARENT = "#999999"
	# colour to be used for the ellipsis where a subtree has been culled
COLOUR_NO_COMM_ANC = "#999999"
	# colour for an individual that does not shared a common ancestor with the focal node
COLOUR_HAS_COMM_ANC = "#3C3736"
	# colour used when an individual shares a common ancestor with the focal node (but is not ancestor itself)
COLOUR_IS_ANC_OR_DESC = "#002DE4"
	# colour when individual is an ancestor or descendant
COLOUR_PRIZE = "#FCC200"
	# colour to be used for prize winners (see PRIZE_WINNER_IDS)


#
#
# Prize winners
#

# The following nodes (if included in the graph) will be coloured differently
PRIZE_WINNER_IDS = [
	'31245',  #31245 		alexander grothendieck         alexander Grothendieck   fields medal
	'60791',  #60791             benoit mandelbrot              benoît mandelbrot   wolf prize
	'31332',  #31332        john archibald wheeler         john archibald wheeler   wolf prize
	'34233',  #34233              laurent schwartz               laurent schwartz   fields medal
	'61289',  #61289           pierre rené deligne                 pierre deligne   abel wolf fields
	'4556',   #4556        richard wesley hamming                richard hamming   turing award
	'91222',  #91222      richard phillips feynman             richard p. feynman   nobel prize physics
	'36928'   #36928                 roger penrose                  roger penrose   wolf prize
	]


#
#
# Seed nodes and other genealogy management
#

# The node who we're building the genealogy for...
ID_FOCAL_NODE = 8014  # Alan Turing

# Nodes whose ancestry will be traced to see if they connect to the focal node's
# ancestry...
SEED_ID_LIST = [
 				 36928, # Roger Penrose
				 12555, # Donald Coxeter
				 91222, # Richard Feynman
				 12543, # Markov
				 60791, # Mandelbrot
				 105806, # James Clerk Maxwell
				 7398, # Haskell Curry (student of Hilbert)
				 4556, # Hamming
				 8012, # Stephen Cole Kleene. Brother to Turing.
				 # following = a few students of feynman
				 136442, # hibbs
				 142041, # lomanitz
				 136436, # curtright
				 # following = intesritng children+descendants of Groethendick
				 61289, # deligne
				 76208, # demazure
				]

# CULL_AND_ABOVE --  these nodes and all their ancestors will be removed
# from the graph. An ellipsis will be inserted at the point at which they were
# removed to indicate that part of the genealogy has been intentionally culled.
CULL_AND_ABOVE = [
	# Cull the following are to tidy up the Turing ancestry
	143084, # Werenfels
	129628, # Eglinger
	125408, # Golius
	125416, # Stampioen
	60984, # Weigel
	# Cull the following to tidy up erdos ancestry
	127710, # elert bode
	128986, # andreas planer
	# Cull the following to tidy up mandelbrot ancestry
	33908, # Vito Volterra
	104652, # Louis Jacques Thenard
	7402, #Julius Plucker
	47025, #Karl Christian von Langsdorf
	# Cull the following to tidy up Feynman ancestry
	83827, # Friedrich Hasenorl
	34260, # Jules Tannery
	]
	

# ERASE_INDIVIDUAL -- i.e., remove these nodes. 
# Unlike CULL_AND_ABOVE, this will not insert ellipsis where the deletion was
# made. It will also not remove any of the erased nodes' successors or parents.
# Erasing a particular individual may disconnect the graph; there is a later
#  step where components that do not reach the focal node are removed, so the
# disconnected component would be erased and would not appear in the output.
ERASE_INDIVIDUAL = [
	146776, # Nikolai Ivanovich Lobachevsky
	151180, # Johann Martin Christian Bartels
	137705, # Thomasius -- creates no-common-ancestory tree. no one interesting.
			# this should partition the uninteresting tree
	]
	


#
#
# Insert extra nodes and connections that do not exist on the Genealogy Project
#

# EXTRA_NODES -- a list of 2-tuples; each is an identifier-label pair. 
# The identifier is used to refer to nodes in the genealogy. The label is the
# text that will appear representing the node in the visualisation.
EXTRA_NODES = [ 
	( '_dummyA', "Dummy Alpha\\nThe Unknown University (1955)" ),
	( '_dummyB', "Dummy Beta\\nThe Unknown University (1980)" ),
	( '_dummyG', "Dummy Gamma\\nThe Unknown University (1983)" ),
	]

# EXTRA_CONNECTIONS -- A list 2-tuples; each is an advisor-student pair. These 
# should be node identifiers.
EXTRA_CONNECTIONS = [
	( '76208', '_dummyB' ),
	( '_dummyA', '_dummyB' ),
	( '_dummyB', '_dummyG' ),
	]






