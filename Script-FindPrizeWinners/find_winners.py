# -*- coding: utf-8 -*- 

import re
import string
import os
import codecs


#
#
# Load list of prize winners
#
fnames = os.listdir(".")
fnames = filter( lambda fn: fn.endswith('.txt'), fnames )
winners = set()
for fname in fnames:
    f = codecs.open( fname, encoding='utf-8', mode='r' )
    for winner in f.read().split('\n'):
        winners.add( winner )
    f.close()

    print "%s unique winners after loading %s" % ( len(winners), fname )
print 


#
#
# List of academics in the genealogy (taken from dot file)
#
people = u"""
		60985 [label="Gottfried Wilhelm Leibniz \nAcadémie royale des sciences de Paris (1676)"];
		53410 [label="Johann Bernoulli \nUniversität Basel (1690)"];
		18253 [label="Philip Hall \nUniversity of Cambridge (1926)"];
		24555 [label="Jacques Salomon Hadamard \nÉcole Normale Supérieure Paris (1892)"];
		4556 [label="Richard Wesley Hamming \nUniversity of Illinois at Urbana-Champaign (1942)"];
		17981 [label="Jean-Baptiste Joseph Fourier \nÉcole Normale Supérieure"];
		17865 [label="Simeon Denis Poisson \nÉcole Polytechnique (1800)"];
		17864 [label="Joseph Louis Lagrange \nUniversità di Torino (1754)"];
		7865 [label="H. A. (Hubert Anson) Newton \nYale University (1850)"];
		missing_parent_0 [label=""];
		36928 [label="Roger Penrose \nUniversity of Cambridge (1958)"];
		17975 [label="Richard Rado \nUniversität Berlin, University of Cambridge (1933)"];
		86693 [label="Henri Léon Lebesgue \nUniversité Henri Poincaré Nancy 1 (1902)"];
		5885 [label="Oskar Bolza \nGeorg-August-Universität Göttingen (1886)"];
		17946 [label="Gustav Peter Lejeune Dirichlet \nRheinische Friedrich-Wilhelms-Universität Bonn (1827)"];
		17829 [label="Andrew Russell Forsyth \nUniversity of Cambridge (1881)"];
		42016 [label="William Hopkins \nUniversity of Cambridge (1830)"];
		121201 [label="Benjamin Pulleyn"];
		17467 [label="George Howard Darwin \nUniversity of Cambridge (1871)"];
		7824 [label="Arthur Cayley \nUniversity of Oxford / University College Dublin / Universiteit Leiden"];
		missing_parent_12 [label=""];
		136436 [label="Thomas Lynn Curtright \nCalifornia Institute of Technology (1977)"];
		125561 [label="Christiaan Huygens \nUniversiteit Leiden / Université d'Angers (1647)"];
		55185 [label="Joseph Liouville \nFaculté des Sciences, Paris (1836)"];
		8014 [label="Alan Mathison Turing \nPrinceton University (1938)"];
		8012 [label="Stephen Cole Kleene \nPrinceton University (1934)"];
		8011 [label="Alonzo Church \nPrinceton University (1927)"];
		42661 [label="A. Donald Keedwell \nUniversity of London (1963)"];
		39071 [label="Émile Borel \nÉcole Normale Supérieure Paris (1893)"];
		98955 [label="Roger Marcus Whitaker \nUniversity of Keele (1999)"];
		133301 [label="Thomas Postlethwaite \nUniversity of Cambridge (1756)"];
		133302 [label="Vincenzo Viviani \nUniversità di Pisa (1642)"];
		133303 [label="Gilles Personne de Roberval"];
		143630 [label="Friedrich Leibniz \nUniversität Leipzig (1622)"];
		61289 [label="Pierre René Deligne \nUniversité Paris-Sud XI - Orsay (1972)"];
		52887 [label="Daniel Segal \nUniversity of London (1972)"];
		137705 [label="Jakob Thomasius \nUniversität Leipzig (1643)"];
		missing_parent_8 [label=""];
		missing_parent_9 [label=""];
		missing_parent_6 [label=""];
		missing_parent_7 [label=""];
		missing_parent_4 [label=""];
		missing_parent_2 [label=""];
		missing_parent_3 [label=""];
		31245 [label="Alexander Grothendieck \nUniversité Henri Poincaré Nancy 1 (1953)"];
		missing_parent_1 [label=""];
		19964 [label="Rudolf Otto Sigismund Lipschitz \nUniversität Berlin (1853)"];
		4544 [label="Waldemar Joseph Trjitzinsky \nUniversity of California, Berkeley (1926)"];
		26995 [label="Michel Chasles \nÉcole Polytechnique (1814)"];
		34233 [label="Laurent Schwartz \nUniversité Louis Pasteur - Strasbourg I (1943)"];
		21235 [label="Otto Mencke \nUniversität Leipzig (1665)"];
		136575 [label="Benedetto Castelli \nUniversità di Padova (1610)"];
		51538 [label="Bertram A. F. Wehrfritz \nUniversity of London (1966)"];
		38586 [label="Leonhard Euler \nUniversität Basel (1726)"];
		28706 [label="Michael Rapoport \nUniversité Paris-Sud XI - Orsay (1976)"];
		108266 [label="Jean Le Rond d'Alembert"];
		143011 [label="Nicolas Malebranche \n(1672)"];
		31332 [label="John Archibald Wheeler \nThe Johns Hopkins University (1933)"];
		156032 [label="William Thornton Shaw \nUniversity of Oxford (1984)"];
		134975 [label="Galileo Galilei \nUniversità di Pisa (1585)"];
		7404 [label="C. L. Ferdinand (Carl Louis) Lindemann \nFriedrich-Alexander-Universität Erlangen-Nürnberg (1873)"];
		7401 [label="C. Felix (Christian) Klein \nRheinische Friedrich-Wilhelms-Universität Bonn (1868)"];
		34266 [label="C. Émile (Charles) Picard \nÉcole Normale Supérieure Paris (1877)"];
		129422 [label="Henry Bracken"];
		129421 [label="Edward Waring \nUniversity of Cambridge (1760)"];
		103066 [label="John Cranke \nUniversity of Cambridge (1774)"];
		103067 [label="Roger Cotes \nUniversity of Cambridge (1706)"];
		103068 [label="Robert Smith \nUniversity of Cambridge (1715)"];
		73816 [label="Georges Valiron \nUniversité de Paris (1914)"];
		7398 [label="Haskell Brooks Curry \nGeorg-August-Universität Göttingen (1930)"];
		74313 [label="Isaac Newton \nUniversity of Cambridge (1668)"];
		133368 [label="Walter Taylor \nUniversity of Cambridge (1723)"];
		133367 [label="Stephen Whisson \nUniversity of Cambridge (1742)"];
		53239 [label="Marcus Peter Francis du Sautoy \nUniversity of Oxford (1989)"];
		136245 [label="Ostilio Ricci \nUniversita' di Brescia"];
		142041 [label="Giovanni Rossi Lomanitz \nCornell University (1950)"];
		125450 [label="Frans van Schooten \nUniversiteit Leiden (1635)"];
		54440 [label="Jacob Bernoulli \nUniversität Basel (1684)"];
		146036 [label="Giovanni Battista (Giambattista) Beccaria"];
		102036 [label="Thomas Jones \nUniversity of Cambridge (1782)"];
		102037 [label="John Dawson"];
		30175 [label="Sir Francis Galton \nUniversity of Cambridge (1847)"];
		30176 [label="Karl Pearson \nUniversity of Cambridge (1879)"];
		102043 [label="Adam Sedgwick \nUniversity of Cambridge (1811)"];
		18571 [label="Edmund Taylor Whittaker \nUniversity of Cambridge (1895)"];
		30473 [label="David E. Daykin \nUniversity of Reading (1961)"];
		17806 [label="G. H. (Godfrey Harold) Hardy \nUniversity of Cambridge"];
		57670 [label="Christian August Hausen \nMartin-Luther-Universität Halle-Wittenberg (1713)"];
		154455 [label="Evangelista Torricelli \nUniversità di Roma La Sapienza"];
		7298 [label="David Hilbert \nUniversität Königsberg (1885)"];
		60791 [label="Benoit Mandelbrot \nUniversité de Paris (1952)"];
		72669 [label="Johann Christoph Wichmannshausen \nUniversität Leipzig (1685)"];
		47064 [label="Martin Ohm \nFriedrich-Alexander-Universität Erlangen-Nürnberg (1811)"];
		13135 [label="Henry Frederick Baker \nUniversity of Cambridge"];
		33053 [label="Paul Pierre Lévy \nUniversité de Paris (1911)"];
		105806 [label="James Clerk Maxwell \nUniversity of Cambridge (1854)"];
		136442 [label="Albert Roach Hibbs \nCalifornia Institute of Technology (1955)"];
		806 [label="E. H. (Eliakim Hastings) Moore \nYale University (1885)"];
		143859 [label="Bartholomäus Leonhard Schwendendörffer \nUniversität Leipzig (1656)"];
		18530 [label="Kurt August Hirsch \nUniversity of Cambridge (1937)"];
		805 [label="Oswald Veblen \nThe University of Chicago (1903)"];
		49353 [label="Andrew Philip Hodges \nUniversity of London (1975)"];
		34254 [label="Gaston Darboux \nÉcole Normale Supérieure Paris (1866)"];
		58739 [label="Paul Montel \nUniversité Paris IV-Sorbonne (1907)"];
		31267 [label="Jean-Louis Verdier \nUniversité de Paris (1967)"];
		108295 [label="Pierre-Simon Laplace"];
		missing_parent_10 [label=""];
		missing_parent_11 [label=""];
		missing_parent_13 [label=""];
		76208 [label="Michel Demazure \nUniversité de Paris (1965)"];
		100550 [label="Eugène-Charles Catalan \nUniversité de Paris (1841)"];
		91222 [label="Richard Phillips Feynman \nPrinceton University (1942)"];
		49477 [label="Kenneth Paul Tod \nUniversity of Oxford (1975)"];
		125434 [label="Marin Mersenne \nUniversité Paris IV-Sorbonne (1611)"];
		35462 [label="Max Dessoir \nUniversität Berlin (1889)"];
		18505 [label="John Arthur Todd \nUniversity of Cambridge (1932)"];
		34219 [label="Jean Alexandre Eugène Dieudonné \nÉcole Normale Supérieure Paris (1931)"];
		67643 [label="Isaac Barrow \nUniversity of Cambridge (1652)"];
		83988 [label="David Bedford \nUniversity of Surrey (1991)"];
		136514 [label="Nicolò Fontana Tartaglia"];
		31354 [label="Augustus Edward Hough Love \nEidgenössische Technische Hochschule Zürich"];
		31357 [label="Arnold Johannes Wilhelm Sommerfeld \nUniversität Königsberg (1891)"];
		23585 [label="Anthony J. W. Hilton \nUniversity of Reading (1967)"];
		12555 [label="H. S. M. (Harold Scott MacDonald) Coxeter \nUniversity of Cambridge (1931)"];
		32845 [label="John Hector McDonald \nThe University of Chicago (1900)"];
		63786 [label="Karl Ferdinand Herzfeld \nUniversität Wien (1914)"];
"""
lines = people.split(';\n')
people = []
for ln in lines:
    m = re.search( r""".*\[label="(.*)[\n\""].*""", ln ) 
    if m is not None:
        person = m.group(1)
        if person:
            people.append( person )
people = map( unicode.lower, people )
people = map( unicode.strip, people )
people = set( people )


#
#
# Compare academics from genealogy to prize winners  -- fuzzy matching
# (edit distance) on last name
#

def levenshtein(seq1, seq2):
    # edit distance
    # via: http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]

def match( a, b, max_dist=2 ):
    lastA = re.split( '[\s \t ]+', a )[-1]
    lastB = re.split( '[\s \t ]+', b )[-1]

    assert len(lastA), "-"+a+"-"
    assert len(lastB), "-"+b+"-"
    dist = levenshtein(lastA, lastB)

    if dist <= max_dist:
        return True
    else:
        return False

for b in winners:
    for a in people:
        if match(a,b):
            print "%30s %30s" % (a,b)
