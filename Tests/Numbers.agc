//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
123.456        //       Match all of this.
0.123          //       Match all of this.

1.             //       Match all of this.
123.           //       Match all of this.
-1.            //       Match all of this.
-123.          //       Match all of this.
.1             //       Match all of this.
-.1            //       Match all of this.
.123           //       Match all of this.
-.123          //       Match all of this.

123.123.123    //       Match all of this.

-1             //       Match all of this.
-123           //       Match all of this.
 -123          //       Match all of this.
 -1            //       Match all of this.

-abc    -abc   //       Match minus here.
-xyz    -xyz   //       Match minus here.   Blarg, I give up...

abc123         // DON'T Match any of this.
123abc         // DON'T Match any of this.

Abc123.x       // DON'T Match any of this.
Abc123.y       // DON'T Match any of this.
Ab1[123].a1.b2 // DON'T Match any of this.  (Brackets are matched separately.)
Abc12.z89.ijk  // DON'T Match any of this.

- - - -        // DON'T Match lone minus.
 - - -
+ + + +        // DON'T Match lone plus.
 + + +
. . . .        // DON'T Match lone dot.
 . . .

1-1            // DON'T Match minus here.
456-456        // DON'T Match minus here.
1-.1           // DON'T Match minus here.
4.6-5.9        // DON'T Match minus here.
45.56-45.96    // DON'T Match minus here.

1+1            // DON'T Match plus here.
123+132        // DON'T Match plus here.
1+.1           // DON'T Match plus here.
2.9+1.2        // DON'T Match plus here.
12.93+13.52    // DON'T Match plus here.

abc.abc        // DON'T Match dots with letters.
xyz.xyz        // DON'T Match dots with letters.
abc.xyz        // DON'T Match dots with letters.
xyz.abc        // DON'T Match dots with letters.
abc.           // DON'T Match dots with letters.
xyz.           // DON'T Match dots with letters.
.abc           // DON'T Match dots with letters.
.xyz           // DON'T Match dots with letters.


//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
%1010101010
 %1010101010

%1010101010+%1010101010
%1010101010-%1010101010

Abc = %1010101010

1%1010101010       // Blarg, none of these are valid anyhow...
01011%1010101010   // Blarg, none of these are valid anyhow...
3%1010101010       // Blarg, none of these are valid anyhow...
76573%1010101010   // Blarg, none of these are valid anyhow...
z%1010101010
%1010101010g


//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
0xA1B2C3D4
 0xA1B2C3D4

0xA1B2C3D4+0xA1B2C3D4
0xA1B2C3D4-0xA1B2C3D4

Ijk = 0xA1B2C3D4

10xA1B2C3D4
z0xA1B2C3D4
0xA1B2C3D4g

