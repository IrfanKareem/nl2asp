export OPENAI_API_KEY=""

STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY")

if [ "$STATUS" = "200" ]; then
  echo "[API KEY]: Verified"
elif [ "$STATUS" = "401" ]; then
  echo "[API KEY]: Invalid"
else
  echo "Error $STATUS"
fi
