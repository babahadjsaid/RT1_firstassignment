# Research Track 1 First Assignment
This repository contains my solution to the given problem, which is to make the robot pair up<br/> Golden and Silver Boxes
## The pseudo code for the solution is as follows:
### Global Variable:
history: is a dict that contains the history of silver and golden silver 
StringF: is a list contains the strings of "Silver" and "Golden" for encoding
### Main Function
<pre>
iter = 0
While size(history_of_golden[]) < 6
  while NNPB(iter%2)< 0
    turn()
  if(GAGTNM(iter%2) == -1)
    repeat loop
  if iter%2==0
    rotate(90 degrees)
  iter++
print finished
exit
</pre>
### Function GAGTNM (Go And Grab The Nearest Marker)
<pre>
  dist,angle,T_code = NNPB(iter)
  Rotate(speed,angle)
  while dist > d_th:
    drive(step)
    if iter == 0 and dist < d_th:
      R.grab()
      history.append(T_code)
      break
    if dist < 1.2*d_th and iter==1:
      R.release()
      history.append(T_code)
      break
</pre>
### Function NNPB (Nearest Non Paired Box)
<pre>
define dist,angle,token_code
for token in R.see()
  if token_distance < dist and token_Flag == TheFlag and token_code not in history
    update dist,angle,token_code
if dist == 100
  return -1
else 
  return dist,angle,token_code
</pre>
### rotate function 
<pre>
seconds = R.width * (angle/speed)
turn(speed,angle)
</pre>

## Some possible improvment 
The code can be further improved by many ways, two of them are:<br/>
  1- By driving and implementing the drive method, so that we can get rid of the nasted while loops.(GoTo function)<br/>
  2- Can improve the recognition of paired boxes by calculating the distance between two diffrent colored boxes