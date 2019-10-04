
#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>

FILE *f;

int main (void)
{
        void *context_s = zmq_ctx_new ();
        void *sender = zmq_socket (context_s, ZMQ_REP);
        int rc = zmq_bind (sender, "tcp://0.0.0.0:5000");
        long int N = 120000;
	char buffer[400];
	int i;
	char **lbuffer = (char**) calloc(N, sizeof(char*));
	for ( i = 0; i < N; i++ )
	{
		lbuffer[i] = (char*) calloc(400, sizeof(char));
	}
	char name[50];
	long int packCount = 0;
	strcpy(buffer, "");
	while (packCount < 120000) {
		zmq_recv (sender, buffer, 400, 0);
		sprintf(lbuffer[packCount], buffer);
		sprintf(buffer, "");
		zmq_send (sender, strcpy(buffer, "Ok"), 3, 0);
		packCount = packCount + 1;
	}
	sprintf(name, "/home/muNet/LAB/pedData");
	f = fopen(name, "a+"); 
	packCount = 0;
	while (packCount < 120000) {
		fprintf (f, "%s", lbuffer[packCount]);
		packCount = packCount + 1;
	}
	fclose(f);
	sleep(1);
    	return 0;
}

