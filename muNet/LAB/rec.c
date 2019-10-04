#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>

int main (void)
{
	//void *context_r = zmq_ctx_new ();
        //void *responder = zmq_socket (context_r, ZMQ_REQ);
        //int rc_r = zmq_connect (responder, "tcp://192.168.0.115:5000");
        //assert (rc_r == 0);
        void *context_s = zmq_ctx_new ();
        void *sender = zmq_socket (context_s, ZMQ_REP);
        int rc = zmq_bind (sender, "tcp://0.0.0.0:5000");
        int count = 0;
        char buffer[10];
	strcpy(buffer, "");
	while (count < 5) {
		zmq_recv (sender, buffer, 10, 0);
		printf ("Received %s\n", buffer);
		zmq_send (sender, strcat(buffer, "Ok"), 10, 0);
		//sleep(1);
		count = atoi(buffer);
    	}
	sleep(1);
    	return 0;
}

