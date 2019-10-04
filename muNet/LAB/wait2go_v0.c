
#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>

int main (void)
{
        void *context_s = zmq_ctx_new ();
        void *sender = zmq_socket (context_s, ZMQ_REP);
        int rc = zmq_bind (sender, "tcp://0.0.0.0:5000");
        char buffer[18];
	strcpy(buffer, "");
	zmq_recv (sender, buffer, 18, 0);
	printf ("%s\n", buffer);
	zmq_send (sender, strcpy(buffer, "Ok"), 10, 0);
	sleep(1);
    	return 0;
}

