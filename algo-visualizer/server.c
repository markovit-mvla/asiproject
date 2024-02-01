#include <errno.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 8080

void error(char *msg);
void error(char *msg) {
    perror(msg);
    exit(1);
}

int init_channel(char *ip, int port, char *name, char *bitstr);
int init_channel(char *ip, int port, char *name, char *bitstr) {
    struct sockaddr_in server;

    server.sin_addr.s_addr = inet_addr(ip);
    server.sin_family = AF_INET;
    server.sin_port = htons(port);

    int channel = socket(AF_INET, SOCK_STREAM, 0);

    if (channel < 0) {
        error("socket");
    }

    int connection_status = connect(channel, (const struct sockaddr *)&server, sizeof(server));

    if (connection_status < 0) {
        error("connect");
    }

    respond(channel, bitstr);
    return channel;
}

char* BB84();
char* BB84() {
    return '0';
}

char* TM99();
char* TM99() {
    return '0';
}

int main(int argc, char** argv) 
{

}