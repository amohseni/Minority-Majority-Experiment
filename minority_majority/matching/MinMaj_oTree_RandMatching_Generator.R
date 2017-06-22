###################################################
# Min/Maj | oTree | Random Matching Generator
###################################################
# by Aydin Mohseni
# July 2016

###################################################
# Variables
###################################################

# Set up the number of rounds of play
RoundsOfPlay <- 120

# Set up the total number of participants in the experiment
GroupSize <- 8

# Set the number of participants in the minority and majority groups
MinorityGroupSize <- 2
MajorityGroupSize <- 6

###################################################
# Generating the Random Matching Table
###################################################

# Create an empty matrix
MatchingTable <- matrix( nrow = RoundsOfPlay, ncol = GroupSize )

# Determine the number of times you will need to randomly (without replacement) match the minority and majority groups
# given the number of rounds of play
randomCycleNum <- ceiling( RoundsOfPlay * MinorityGroupSize / ( GroupSize - MinorityGroupSize ) )
# Create matchings of the minority player with majority players
MinorityGroupOrder <- as.numeric( replicate( randomCycleNum, {
  sample( ( MinorityGroupSize + 1 ) : GroupSize, GroupSize - MinorityGroupSize, replace=FALSE )
} ) )
# If the number of matchings is more than the rounds of play, then truncate the surplus rounds of matchings
if ( length(MinorityGroupOrder) > (RoundsOfPlay * MinorityGroupSize ) ) {
  surplusMatchings <- length( MinorityGroupOrder) - ( MinorityGroupSize * RoundsOfPlay )
  MinorityGroupOrder <- head( MinorityGroupOrder, -surplusMatchings ) 
}
# reshape the MinorityGroupOrder vector into a matrix 
# with rows corresponding to rounds, and columns corresponding to players
dim( MinorityGroupOrder ) <- c( MinorityGroupSize, RoundsOfPlay ) 
MinorityGroupOrder <- t( MinorityGroupOrder ) # transpose the MinorityGroupOrder vector

# Insert the minority group matching matrix into the MatchingTable
MatchingTable[ 1:RoundsOfPlay, 1:MinorityGroupSize ] <- MinorityGroupOrder

# Create the corresponding matching vector for the majority group, 
# where majority members who are not matched sit out (receive a 0 for their partner)
for ( i in 1:RoundsOfPlay ) {
  for ( j in ( MinorityGroupSize + 1 ):GroupSize) {
    if ( j %in% MatchingTable[ i, ] ) {
      MatchingTable[ i, j ] <- match( j, MatchingTable[i, ] )
    }
    else {
      MatchingTable[ i, j ] <- 0
    }
  }  
}
print( MatchingTable )

# Reformat the matching table in terms of 'groups matchings' 
# that are intelligible for oTree.
# First, replace the numbers in the first two columns by their corresponding group numbers 
# (which will just be the player number [since these are the minority group players])
for ( i in 1:MinorityGroupSize ) {
  MatchingTable[ , i ] <- rep( i, RoundsOfPlay )
}
# Next, replace the zeroes in the rest of the table with the number for the group that sits out
MatchingTable[ MatchingTable == 0 ] <- ( MinorityGroupSize + 1 )
print( MatchingTable )

###################################################
# Converting to oTree-Readable Style
###################################################

MatchingTableOTree <- matrix( nrow = RoundsOfPlay, ncol = 2*GroupSize )

for ( i in 1:RoundsOfPlay){
  MatchingTableOTree[i,1:2] <- which(MatchingTable[i,]==1)
  MatchingTableOTree[i,3:4] <- which(MatchingTable[i,]==2)
  MatchingTableOTree[i,5:8] <- which(MatchingTable[i,]==3)
}

MatchingTableOTree[,9:16] <- MatchingTableOTree[,1:8]+8

###################################################
# Writing the Spreadsheet CSV
###################################################

# Set the working directory
setwd( "/Users/aydin/Desktop" )

# Write a CSV file of the final matching table
write.table( MatchingTable, file = paste( "MatchingTable", "_min", MinorityGroupSize, "_maj", MajorityGroupSize, "_r", RoundsOfPlay, ".csv", sep = "" ), 
             sep = ', ', row.names = F, col.names = F )
# Write a CSV file of the final matching table [for oTree]
write.table( MatchingTableOTree, file = paste( "oTreeMatchingTable", "_min", MinorityGroupSize, "_maj", MajorityGroupSize, "_r", RoundsOfPlay, ".csv", sep = "" ), 
             sep = ', ', row.names = F, col.names = F )
