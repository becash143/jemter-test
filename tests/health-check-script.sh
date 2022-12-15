set -e

while ! curl -sSL "http://hub:4444/wd/hub/status" 2>&1 \
    | jq -r '.value.ready' 2>&1 | grep "true" >/dev/null; do
    echo 'Waiting for the Grid'
    sleep 1
done
while ! curl -sSL "http://keycloak-local:8080/auth/realms/master/protocol/openid-connect/auth?client_id=annotationlab&response_type=code&redirect_uri=http://annotationlab:8200/getUserToken" 2>&1 \
    | grep '<input tabindex="1" id="username" class="form-control" name="username" value=""  type="text" autofocus autocomplete="off"
                               aria-invalid=""
                        />' >/dev/null;
   do echo "Waiting for keycloak"
   sleep 4
done
    echo "Selenium Grid is up - executing tests"
