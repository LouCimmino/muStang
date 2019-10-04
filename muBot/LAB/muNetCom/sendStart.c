#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <time.h>
#include <stdlib.h>
int main (int argc, char *argv[])
{   
    char msg[23];
    char buffer[10];
    int rc;
	//  Socket to talk to clients
    void *context = zmq_ctx_new ();
    void *responder = zmq_socket (context, ZMQ_REQ);

     if (strcmp(argv[1], "ROSSO") == 0) {
	rc = zmq_connect (responder, "tcp://192.168.77.1:5000");
	sprintf(msg, "MasterPi03_%s Ready!", argv[1]);
    } else if (strcmp(argv[1], "NERO") == 0) {
	rc = zmq_connect (responder, "tcp://192.168.77.1:6000");
	sprintf(msg, "MasterPi04_%s Ready!", argv[1]);
    } else if (strcmp(argv[1], "BLU") == 0) {
	rc = zmq_connect (responder, "tcp://192.168.77.1:7000");
	sprintf(msg, "MasterPi05_%s Ready!", argv[1]);
    }
    assert (rc == 0);
    zmq_send (responder, msg, 23, 0);
    zmq_recv (responder, buffer, 10, 0);
    //printf ("%s\n",buffer);
    return 0;
}

