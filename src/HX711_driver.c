sbit   ADDO = P1^5; 
sbit   ADSK = P0^0; 
unsigned long ReadCount(void){   
  unsigned long Count;   
  unsigned char i;   
  ADDO=1;              
  ADSK=0;   
  Count=0;   
  while(ADDO);   
  for (i=0;i<24;i++){     
    ADSK=1;     
    Count=Count<<1;     
    ADSK=0;     
    if(ADDO) Count++;   
  }   
  ADSK=1;   
  Count=Count^0x800000;    
  ADSK=0;   
  return(Count); 
}
