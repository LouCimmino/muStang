#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "libreriaSC_EASI.h"

  void main(int argc, char **argv) {
  FILE *f;

  unsigned short SC_EASI[456];
  unsigned short ReversedSC_EASI[456];
  unsigned short PR_EASI[160];
  unsigned short ReversedPR_EASI[160];
  unsigned short hexSC_EASI[120];
  unsigned short hexPR_EASI[44];
  int i = 0;
  int j = 0;
  int error;

  for (i=0; i<456; i++) SC_EASI[i]=0;
  for (i=0; i<160; i++) PR_EASI[i]=0;

  for (i=0; i<118; i++) hexSC_EASI[i]=0x0;
  for (i=0; i<44; i++) hexPR_EASI[i]=0x0;

  initSC_EASI(SC_EASI);
  
  for (i=0; i<32; i++) error = DACbiasSC_EASI(SC_EASI, i, 145);
  error = DACbiasSC_EASI(SC_EASI, 4, 160);
  //error = DACbiasSC_EASI(SC_EASI, 3, 0);
  error = DACbiasSC_EASI(SC_EASI, 19, 180);
  error = DACbiasSC_EASI(SC_EASI, 28, 120); //180
  error = DACbiasSC_EASI(SC_EASI, 30, 160);
  error = DACbiasSC_EASI(SC_EASI, 31, 130);
  error = DACbiasSC_EASI(SC_EASI, 12, 140);
  error = DACbiasSC_EASI(SC_EASI, 14, 140);
  //error = DACbiasSC_EASI(SC_EASI, 25, 0);
  error = DACbiasSC_EASI(SC_EASI, 26, 140);
  error = DACbiasSC_EASI(SC_EASI, 27, 140);
  error = DACbiasSC_EASI(SC_EASI, 17, 150);
  error = DACbiasSC_EASI(SC_EASI, 24, 150);
  
  for (i=0; i<32; i++) DACswitchSC_EASI(SC_EASI, i, 1); // 1 = ON
  for (i=0; i<32; i++) PAMPdisSC_EASI(SC_EASI, i, 0); // 0 = enabled
  for (i=0; i<32; i++) TCAPenblSC_EASI(SC_EASI, i, 0); // 0 = testcap off
  
  HGtimecSC_EASI(SC_EASI, 6);
  for (i=0; i<32; i++) DISCRmaskSC_EASI(SC_EASI, i, 1); // 1 = nomask
  
//DAC10
	DAC10thrsSC_EASI(SC_EASI,0);
  
  setPR_EASI(PR_EASI, 0, 9);// con 9  il file di prob e' tutti 0 tranne il comando

  ReverseSC_EASI(SC_EASI, ReversedSC_EASI);
  ReversePR_EASI(PR_EASI, ReversedPR_EASI);

  SCtoHEXSC(hexSC_EASI, ReversedSC_EASI);
  PRtoHEXPR(hexPR_EASI, ReversedPR_EASI);  

  hexSC_EASI[118]=hexSC_EASI[119]=0;
  f = fopen("Core/EASI_DAC8.txt", "w");
  
  for (i=0; i<120; i++) {
    if (i%4 == 0 && i !=0) fprintf(f, "\n");
	fprintf(f, "%x", hexSC_EASI[i]);
  }
  fclose(f);
  
  
}
