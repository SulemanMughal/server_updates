#!/usr/bin/bash

new_client () {
        # Generates the custom client.ovpn
        {
        cat /etc/openvpn/server/client-common.txt
        echo "<ca>"
        cat /etc/openvpn/server/easy-rsa/pki/ca.crt
        echo "</ca>"
        echo "<cert>"
        sed -ne '/BEGIN CERTIFICATE/,$ p' /etc/openvpn/server/easy-rsa/pki/issued/"new".crt
        echo "</cert>"
        echo "<key>"
        cat /etc/openvpn/server/easy-rsa/pki/private/"new".key
        echo "</key>"
        echo "<tls-crypt>"
        sed -ne '/BEGIN OpenVPN Static key/,$ p' /etc/openvpn/server/tc.key
        echo "</tls-crypt>"
        } > ../media/"new".ovpn
}


unsanitized_client="$1"
client=$(sed 's/[^0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-]/_/g' <<< "$unsanitized_client")
while [[ -z "new" || -e /etc/openvpn/server/easy-rsa/pki/issued/"new".crt ]]; do
    # echo "new: invalid name."
    read -p "Name: " unsanitized_client
    client=$(sed 's/[^0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-]/_/g' <<< "$unsanitized_client")
done
cd /etc/openvpn/server/easy-rsa/
/usr/share/easy-rsa/easyrsa --batch --days=3650 build-client-full "new" nopass
# Generates the custom client.ovpn
new_client
# echo
# echo "/home/suleman/Downloads/updated/crfront/cys_games/new.ovpn"
exit
