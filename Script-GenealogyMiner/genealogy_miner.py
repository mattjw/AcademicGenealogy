# -*- coding: utf-8 -*-

import re
import codecs
import sys
import argparse

import networkx as nx
from geneagrapher import geneagrapher

from config import *


#
#
# GLOBAL CONSTS
#
TMP_DOT_FPATH = "./_tmp.dot"
DOT_TEMPLATE = u"""
digraph genealogy {
\t\tgraph [charset="utf-8"];
\t\tnode [shape=plaintext];
\t\tedge [style=bold];

<nodes>

<edges>
}
"""


#
#
# INPUT
#

parser = argparse.ArgumentParser(description="Batch Grader")

# compulsory
parser.add_argument( 'input_py_module', action='store', type=str,
                     help="Input configuration file, as Python module" )
parser.add_argument( 'output_dot_file', action='store', type=str,
                     help="Output genealogy, as DOT file" )

args = parser.parse_args()
FCONFIG_PATH = args.input_py_module.rstrip('.py')
FOUT_PATH = args.output_dot_file

config = __import__(FCONFIG_PATH)

#
#
# FUNCS
#
def get_leaves( nxg, node_id ):
	"""
	Get all leaves of the tree rooted at node_id.
	"""
	def rec( nxg, n ):
		succ = nxg.successors( n )
		if not succ:
			return [n] # no successors. thus this is a leaf
		else:
			return reduce( list.__add__, map( lambda x: rec(nxg,x), succ ) )
	return rec(nxg,node_id)


def get_roots( nxg, node_id ):
	"""
	Get all root noes above node_id.
	"""
	def rec( nxg, n ):
		pred = nxg.predecessors( n )
		if not pred:
			return [n] # no predecessors. thus this is a root
		else:
			return reduce( list.__add__, map( lambda x: rec(nxg,x), pred ) )
	return rec(nxg,node_id)


def colour_descendants( nxgraph, node_id, colour ):
	"""
	Traverse all descendants from node_id and colour them with `colour`.
	"""
	def rec( nxg, n ):
		# If this node is already coloured in the correct colour, 
		# we assume all its desc are coloured and stop recursion
		if 'colour' in nxg.node[n]:
			if nxg.node[n]['colour'] == colour:
				return 

		# Colour this node
		nxg.node[n]['colour'] = colour

		succ = nxg.successors( n )

		# If there are no successors, we're done
		if not succ:
			return

		# Colour the edges to successors and recuse on each
		for s in succ:
			nxg.edge[n][s]['colour'] = colour
			rec( nxg, s )

	rec( nxgraph, node_id )


def colour_ancestors( nxgraph, node_id, colour ):
	"""
	Traverse all ancestors from node_id and colour them with `colour`.
	"""
	def rec( nxg, n ):
		# If this node is already coloured in the correct colour, 
		# we assume all its desc are coloured and stop recursion
		if 'colour' in nxg.node[n]:
			if nxg.node[n]['colour'] == colour:
				return 

		# Colour this node
		nxg.node[n]['colour'] = colour

		preds = nxg.predecessors( n )

		# If there are no successors, we're done
		if not preds:
			return

		# Colour the edges to successors and recuse on each
		for p in preds:
			nxg.edge[p][n]['colour'] = colour
			rec( nxg, p )

	rec( nxgraph, node_id )


def nxgraph_to_dot( nxg, focal_node_id ):
	"""
	Take a networkx graph `nxg` and convert it to a dot file representation.
	The representation is returned as a string.

	This also involves...
	
	* Colouring nodes according to the colour scheme (see COLOUR_* variables).
	  The `focal_node_id` parameter is used in this processes. This is the 
	  node to which ancestry / lineage, common ancestorship, etc., are checked. 
	"""
	
	txt = DOT_TEMPLATE

	# 
	# Compute node and edge colours based on their position (common anc, anc, etc.)
	# Colours are inserted into nxg as attribute 'colour'
	
	# 1 - Find leaves of the subtree rooted at focal node
	leaves = get_leaves( nxg, focal_node_id )

	# 2 - Find root nodes of the subgraph of ancestors of focal node
	roots = get_roots( nxg, focal_node_id )

	# 3 - Do exclusively DOWNWARD breatdthfirst traversal from each root node
	# colouring the edges and nodes as common ancestors
	for root in roots:
		colour_descendants( nxg, root, config.COLOUR_HAS_COMM_ANC )

	# 4 - do upwards traversal from leaves (step 1) overwritting
	# colours to designate the nodes and edges as direct ancs/descs
	for leaf in leaves:
		colour_ancestors( nxg, leaf, config.COLOUR_IS_ANC_OR_DESC )

	# 5 - any un-coloured nodes and edges are NOT common ancs, so colour them
	# as such
	for node in nxg.nodes_iter():
		if 'colour' not in nxg.node[node]:
			nxg.node[node]['colour'] = config.COLOUR_NO_COMM_ANC

	for frmID,toID in nxg.edges_iter():
		if 'colour' not in nxg.edge[frmID][toID]:
			nxg.edge[frmID][toID]['colour'] = config.COLOUR_NO_COMM_ANC

	# 6 - colour missing parents 
	for frmID, toID in nxg.edges_iter():
		if frmID.startswith( 'missing_parent' ) or toID.startswith( 'missing_parent' ):
			nxg.edge[frmID][toID]['colour'] = config.COLOUR_MISSING_PARENT
	
	# (7 - overwrite colour for prize winners)
	for node in nxg.nodes_iter():
		if node in config.PRIZE_WINNER_IDS:
			nxg.node[node]['colour'] = COLOUR_PRIZE

	#
	# Write each node and edge out...

	txt_nodes = u""
	for nodeID, dct in nxg.nodes_iter(data=True):
		#print nodeID, dct
		#print type(nodeID), type(dct)

		label = dct['label']
		
		# Do something special for an ellipsis?
		if label == '...':
			label = '...'  # just leave it alone!

		# Finish up....
		label = re.sub( r'\s+', ' ', label )
		colour = nxg.node[nodeID]['colour']
		s = u"""\t\t%s [label="%s" fontcolor="%s"];\n""" % (nodeID,label,colour)

		txt_nodes += s

	txt_edges = u""
	for frmID,toID in nxg.edges_iter():

		colour = nxg.edge[frmID][toID]['colour']
		s = u"""\t\t%s -> %s [color="%s"];\n""" %(frmID,toID,colour)
		
		txt_edges += s

	txt = txt.replace( "<nodes>", txt_nodes )
	txt = txt.replace( "<edges>", txt_edges )

	return txt


def mathID_to_nxgraph( mathID ):
	"""
	Obtain ancestry from the Mathematics Genealogy Project for the individual 
	with Project ID `mathID`. All ancestors for `mathID` are obtained.
	Descendants are NOT crawled.

	A networkx di-graph is returned. Nodes (academics) are defined by their 
	corresponding ID on the Genealogy Project.

	This uses the geneagrapher package by David Alber:
	http://www.davidalber.net/geneagrapher/
	"""
	gg = geneagrapher.Geneagrapher()
	gg.get_ancestors = True
	gg.get_descendants = False
	gg.leaf_ids.append( mathID )
	gg.write_filename = TMP_DOT_FPATH

	gg.buildGraph()
	gg.generateDotFile()

	g = nx.drawing.read_dot( TMP_DOT_FPATH )
	return g


#
#
# PROC
#

#
# Prep

g = nx.DiGraph()

if config.ID_FOCAL_NODE not in config.SEED_ID_LIST:
	config.SEED_ID_LIST.append( config.ID_FOCAL_NODE )

for mathID in config.SEED_ID_LIST:
	print "Crawling ancestry for node %s..." % (mathID)
	g_new = mathID_to_nxgraph( mathID )
		# g_new is a MultiDiGraph, but should not actually have any 
		# multi edges, so just need to add nodes and edges individually

	g.add_nodes_from( g_new.nodes(data=True) )
	g.add_edges_from( g_new.edges(data=True) )
	# "Adding the same edge twice has no effect but any edge data will be 
	# updated when each duplicate edge is added.""


#
# Add extras
for node_id, label in config.EXTRA_NODES:
	g.add_node( node_id, {'label':label}  )

for advisor_id, student_id in config.EXTRA_CONNECTIONS:
	g.add_edge( advisor_id, student_id )


# 
# Cull some nodes and their ancestors
for mathID in config.CULL_AND_ABOVE:
	targetID = str(mathID)
	if targetID in g:
		
		# 
		# Remember children so i can add ellipsis above
		children = set( g.successors( targetID ) )

		#
		# Delete the target and its ancestors
		cull = set( g.predecessors( targetID ) ) | set([targetID])
		for nodeID in cull:
			g.remove_node( nodeID )
		
		#
		# Insert separate ellipsis above children
		# (Nice feature -- later on, turn ellipsis into blank node and turn edge
		# into greyed-out arrow)
		# (Should do same for where i've discarded/not obtaied children?)
		for child in children:
			ellips_id_int = 0
			while ("missing_parent_%s" % ellips_id_int) in g:
				ellips_id_int += 1
			ellips_id = "missing_parent_%s" % ellips_id_int
			g.add_node( ellips_id, {'label':"..."} )
			g.add_edge( ellips_id, child )

# 
# Erase some nodes
for nodeID in config.ERASE_INDIVIDUAL:
	if str(nodeID) in g:
		g.remove_node( str(nodeID) )

#
# Remove any components that do not have the focal node
undir = g.to_undirected()
rmw_component = nx.node_connected_component( undir, str(config.ID_FOCAL_NODE) )

nodes_keepers = set( rmw_component )
nodes_all = set( undir.nodes() )

nodes_cull = nodes_all - nodes_keepers
for cull in nodes_cull:
	if cull in g:
		g.remove_node(cull)

#
# Presentation / output
dot_txt = nxgraph_to_dot( g, str(config.ID_FOCAL_NODE) )

f = codecs.open( FOUT_PATH, encoding='utf-8', mode='w' )
f.write(dot_txt)
f.close()

