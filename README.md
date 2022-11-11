# Research Track 1 First Assignment
This repository contains my solution to the given problem, which is to make the robot pair up<br/> Golden and Silver Boxes
## The pseudo code for the solution is as follows: 
### Main Function
<pre>
while there still unpaired golden box repeat
  while we didn't find unpaired Silver/Golden box keep
    turning
  Go And Grab/release the silver box
  if we just released a silver box
    rotate 90 degrees

When done print finished
exit
</pre>
### Function GAGTNM (Go And Grab The Nearest Marker)
<pre>
  while we are not facing the box keep:
    turning
  while we did not reach the box keep:
    driving
    if we are in the case of silver box and the dist is d_th:
      grab the box 
      add it to the list of paired silver 
      break from the loop 
    if we are in the case of golden box and the dist is 1.5*d_th:
      release the box 
      add it to the list of paired golden
      break from the loop 

</pre>
