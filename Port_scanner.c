*/ code written with chatgpt
edited by aelphias */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define HOST "localhost"
#define PORT_FROM 10000
#define PORT_TO 65000
#define OWN_PORT 45678

int find_available_port() {
    struct sockaddr_in addr;
    int sock;
    for (int port = PORT_FROM; port <= PORT_TO; port++) {
        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = inet_addr(HOST);
        addr.sin_port = htons(port);
        sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (sock < 0) {
            perror("socket");
            exit(1);
        }
        if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
            close(sock);
            return port;
        }
        close(sock);
    }
    return -1;
}

void handle_request(int client_sock) {
    char response[32];
    int port = find_available_port();
    sprintf(response, "%d", port);
    char *http_response =
        "HTTP/1.1 200 OK\r\n"
        "Content-Length: %ld\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        "%s";
    char *response_str =
        (char *)malloc(strlen(http_response) + strlen(response));
    sprintf(response_str, http_response, strlen(response), response);
    send(client_sock, response_str, strlen(response_str), 0);
    free(response_str);
}

int main(int argc, char *argv[]) {
    int server_sock, client_sock;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len;

    server_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (server_sock < 0) {
        perror("socket");
        exit(1);
    }
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(OWN_PORT);
    if (bind(server_sock, (struct sockaddr *)&server_addr,
             sizeof(server_addr)) < 0) {
        perror("bind");
        exit(1);
    }
    if (listen(server_sock, 5) < 0) {
        perror("listen");
        exit(1);
    }

    while (1) {
        client_addr_len = sizeof(client_addr);
        client_sock =
            accept(server_sock, (struct sockaddr *)&client_addr,
                   &client_addr_len);
        if (client_sock < 0) {
            perror("accept");
            exit(1);
        }
        handle_request(client_sock);
        close(client_sock);
    }

    return 0;
}
