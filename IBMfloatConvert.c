1.32 bit IEEE floating format
分三部分：符号位（sign）占1bit，指数部分(exp)占8bits，尾数部分(x)占23bits.
所表示的十进制数值result = (-1)^sign * ( 1 + x / ( 2^23 )   )   * 2 ^ ( exp -127 )
2. 32 bit IBM floating format
分三部分： 符号位(sign)占1 bit, 指数部分(exp )占7bits, 尾数部分(mant)占24 bits.
所得数值result = (-1)^sign * ( mant / (2^24) ) * 16 ^ ( exp - 64 )
3.   十进制浮点数转换为32 bit IEEE floating format
void Form32BitFloat::num2ieee( float dec)
{
      int sign,e;
     uint x;
     // 符号位：负数取1，其他取0。:
     sign =   dec<0?1:0;
        
     //    abs(dec) :
     dec= dec* pow(-1, sign);   
    float d1;        // integer part of float :
     d1=(float)(int )dec;      
     double d2;       // other part of float :
     d2=(double )(dec - d1);
     // gain e : 指数
     int   e0=0;
     int d1d = d1;
     if ( dec >0   ) //非0值才有必要计算
     {
if (d1d >= 1)// d1 will shift right :
{
      while ( d1d>1)
      {
   d1d=(int)d1d/2;
   e0++;
      }
}   
else //   d2 will shift left :
{
      d2d=d2;
      while ((int)d2d!=1)
      {
   d2d*=2;
   e0--;            
      }
}
     }
     e= e0 + 127;
   
     // gain x :
     float x0;
     x0 = dec * pow(2,-e0) - 1 ;
     x = x0 * pow(2, 23 ) ;
   
     if (dec==0)      {x=0 ; e = 0 ;}     //0值特殊对待
   
     // merge sign,e,x:
    ulong result ;
     if ( sign==0)
result = sign*pow(2,31) + e*pow(2,23) + x ;//正值以原码形式存放
     else
result =   (~ e) *pow(2,23) + (~x )    +1 ;// 负值以补码形式存放
}
4. 32 bit IEEE floating format 转换为十进制浮点数
void Form32BitFloat::pushButtonIeee2Decimal_clicked()
{
    ulong ieee;
     ieee=lineEditIEEEFloatInt->text().toULong();
     int sign; //符号
     sign =( ieee& 0x80000000 ) *pow(2,-31);
     if (sign ==1)// for value < 0 :
ieee =~( ieee&0x7fffffff ) ;//负数则为补码
     int e;//指数
     e=(   ieee & 0x7f800000 ) * pow(2,-23) - 127 - sign   ；
     uint x ; //尾数
     x = ieee & 0x007fffff   -sign   ; // - sign : for value < 0
     float x0 ;
     x0 = x* pow(2,-23);
     float result;
     if ( x0 ==0 && e + 127 ==0 ) //0值特殊对待
            result = 0;      
    else
             result = pow(-1,sign)*(1+x0)*pow(2,e);
}
5. 十进制数转 32 bit IBM floating format
void Form32BitFloat::num2ibm(float input)
{
      long sign;//符号
     sign =   ( input<0?1:0 ) ;
      long exp;//指数
      float input1 ; // attention : cannot use   long input1;
     input   = input * pow(-1, sign);// abs(input)
     exp=0;
     input1 = input;
     if (input >0 )    // 非0值才计算
     {
        if( (int)input>0)
       {
           exp++;
           while   ((int) input1/16 > 0)
          {
             exp++;
             input1= input1/16;
           }
      }
     else
       {
               while ( (int)input1*16 ==0)
              {
                    exp--;
                    input1=input1*16;
              }
             exp++;// attention :    ibm fmant   :     0.mant   not 1.mant !
      }
    }
     long e;
     e = (   exp + 64 ) ;
   
      double     fm = input * pow(16,-exp);////////////////
   
     long fmant=(long) (   fm * pow(2,24) ) ;//尾数
     ulong result ;
     result = ( sign<<31) | (   e <<24   )    |   fmant ;     
}
6. IBM 转十进制数
void Form32BitFloat::pushButtonIbm2decimal_clicked()
{   
     ulong DataUint32;      
     DataUint32 = lineEditIBMFloatInt->text().toULong();
         // gain sign from first bit
     double   sign = (double )( DataUint32 >>31) ;     
     // gain exponent from first byte, last 7 bits
     double   exp0 = (double) ( (   DataUint32 &0x7f000000 )   >>24) ;
        // remove bias from exponent  
     double   exp =(double   )(exp0   - 64 )   ;  
     // gain mantissa from last 3 bytes
     double frac = ( double )( DataUint32 &0x00ffffff   ) ;
     double fmant = frac/ (pow(2,24) ) ;
     float   result = ( 1-2*sign)*( pow( 16 ,exp) ) *fmant;
}
7. IEEE to IBM
void Form32BitFloat::ieee2ibm(ulong fconv)
{
     int endian;
     endian=checkBoxBigEndian->isChecked();  
     ulong result ;
     ulong fmant;
     ulong   fff ;  
     fff=0;
     long sign;
     long t0,t ;
     long   exp;   long mant ;
     if (fconv)
     {
          sign = ( 0x80000000 & fconv ) >> 31;
          fmant = (0x007fffff & fconv ) | 0x00800000 ;
          t0 = 0x7f800000 & fconv ;
           t = (long )(t0 >> 23 ) - 126;
          while ( t & 0x3 ) { ++t; fmant >>=1;}
         exp =   t>>2;
           fff = ( 0x80000000 & fconv ) | ((( t>>2) + 64 ) << 24 ) | fmant ;
     }
     if ( endian==0)
           fff=(fff<<24) | ((fff>>24)&0xff) |
                 (( fff&0xff00)<<8) | ((fff&0xff0000)>>8);   
     result = fff;
}
8. 特别说明
以上各算法经过正负整数、小数、0的测试后，发现除IEEE2IBM算法外其他算法皆测试正确。
9. 遗留问题
IEEE2IBM算法对正数可以正确转换，但负数却转换错误！有待进一步分析