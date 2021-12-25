#  Analysis

[n1 n2 n3 n4 n5 n6 n7 n8 n9 n10 n11 n12 n13 n14]
 4  1  2  9  9  9  9  4  8   7   9   9   5   9

 1  1  1  8  9  5  6  1  1   1   3   2  1    6 


   

n3 + 7 = n4
n2 + 8 = n5
n8 + 5 = n7
n10 + 2 = n11
n9 + 1 = n12
n13 + 4 == n6
n1 + 5 == n14

inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 16
mul y x
add z y

z1 = n1 + 16

inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 11
mul y x
add z y

z2 = 26*z1+n2+11

inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1 (1,26)
mul z y
mul y 0
add y w
add y 12
mul y x
add z y

z3 = 26*z2 + n3 + 12

inp w
mul x 0
add x z
mod x 26 x = n3+12
div z 26 z = z2
add x -5 x = n3+7
eql x w  n4 == n3 + 7
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y

if n4 == n3 + 7 then
  z4 = z2
     = 26*z1 + (n2+11)

inp w
mul x 0
add x z
mod x 26
div z 26    z = z1
add x -3    
eql x w     n5 == n2 + 8
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y

if n5 == n2 + 8 then
  z5 = z1
     = n1 + 16

inp w
mul x 0
add x z
mod x 26 x = n1 + n5 + 3
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 2
mul y x
add z y
inp w

z6 = z1*26 + n6 + 2

mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 11
mul y x
add z y
inp w

z7 = z6*26 + n7 + 11

mul x 0
add x z
mod x 26
div z 26
add x -16 x = n7 - 5
eql x w  n8 == n7 - 5
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y

if n8 == n7 - 5
  z8 = z6
     = z1*26 + n6 + 2

inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y

z9 = z8*26 + n9+12

inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y

z10 = z9*26 + n10+9

inp w
mul x 0
add x z
mod x 26 
div z 26
add x -7 x = n10+2
eql x w  n11 == n10 + 2
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y

if n11 == n10 + 2
    z11 = z9
        = z8*26 + n9+12

inp w
mul x 0
add x z
mod x 26
div z 26    
add x -11 n12 == n9 + 12 - 11 = n9 + 1
eql x w   n12 = n9 + 1
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 11
mul y x
add z y

if n12 = n9 + 1
  z12 = z8
      = z1*26 + n6 + 2

inp w
mul x 0
add x z
mod x 26
div z 26
add x -6 x = (n6 + 2) % 26 - 6
eql x w  n13 == n6 - 4
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y

z13 = z1 = n1 + 16

inp w
mul x 0
add x z
mod x 26
div z 26 z = (n1 + 16)/26 = 0
add x -11 x = n1 + 16 - 11
eql x w  n14 == n1 + 5
eql x 0   
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y

