#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <time.h>
#include <stdlib.h>
int main (int argc, char *argv[])
{
    //  Socket to talk to clients
    void *context = zmq_ctx_new ();
    void *responder = zmq_socket (context, ZMQ_REQ);
    //int rc = zmq_connect (responder, "tcp://192.168.77.32:5000");
	int rc = zmq_connect (responder, argv[1]);
    assert (rc == 0);
    char buffer[10];
    //char runs[5];
    //sprintf(runs,"%d",2);
    //zmq_send (responder, runs, 5, 0);
    //zmq_recv (responder, buffer, 10, 0);
    //printf ("%s\n",buffer);
    char peds[5];
    sprintf(peds, argv[2]);
    zmq_send (responder, peds, 5, 0);
    zmq_recv (responder, buffer, 10, 0);
    //printf ("%s\n",buffer);
    char evts[5];
    sprintf(evts, argv[3]);
    zmq_send (responder, evts, 5, 0);
    zmq_recv (responder, buffer, 10, 0);
    //printf ("%s\n",buffer);
    return 0;
}
