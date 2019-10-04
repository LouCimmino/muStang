#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>

FILE *f;

int main (int argc, char *argv[])
{
	void *context_s = zmq_ctx_new ();
	void *sender = zmq_socket (context_s, ZMQ_REP);
	int rc = zmq_bind (sender, argv[1]);
	int count = 0;
	char buffer[10];
	char name[20];
	char dtcFile[50];
	
	//if (argv[2] == "ROSSO") strcpy(dtcFile, "/home/DatiTB/DTC/DTC_ROSSO.txt");
	//else if (argv[2] == "NERO") strcpy(dtcFile, "/home/DatiTB/DTC/DTC_NERO.txt");
	//else if (argv[2] == "BLU") strcpy(dtcFile, "/home/DatiTB/DTC/DTC_BLU.txt");
	sprintf(name, "/home/DatiTB/DTC/DTC_%s.txt", argv[2]);
	f = fopen(name, "w");
	strcpy(buffer, "");
	while (count < 2) {
		zmq_recv (sender, buffer, 10, 0);
		//printf ("Received %s\n", buffer);
		if (count == 0) fprintf(f, "$PEDS\t%s\n", buffer);
		if (count == 1) fprintf(f, "$EVTS\t%s\n", buffer);
		zmq_send (sender, strcat(buffer, "Ok"), 10, 0);
		count = count+1;
    	}
	fclose(f);
	sleep(1);
    return 0;
}

