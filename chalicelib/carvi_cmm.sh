# readJson function parses json file
function readJson {  
  UNAMESTR=`uname`
  if [[ "$UNAMESTR" == 'Linux' ]]; then
    SED_EXTENDED='-r'
  elif [[ "$UNAMESTR" == 'Darwin' ]]; then
    SED_EXTENDED='-E'
  fi; 

  VALUE=`grep -m 1 "\"${2}\"" ${1} | sed ${SED_EXTENDED} 's/^ *//;s/.*: *"//;s/",?//'`

  if [ ! "$VALUE" ]; then
    echo "Error: Cannot find \"${2}\" in ${1}" >&2;
    exit 1;
  else
    echo $VALUE ;
  fi; 
}

# move to previous folder
function upto
{
  if [ -z "$1" ]; then
      return
  fi
  local upto=$1
  cd "${PWD/\/$upto\/*//$upto}"
}


echo "--------------------------------------------------------------------"
echo "|                                                                  |"
echo "|                                                                  |"
echo "|               Welcome to CarVi Microservice Manager              |"
echo "|                             (ver 1.0.0)                          |"
echo "|                                                                  |"
echo "--------------------------------------------------------------------"
echo ""

echo "SELECT THE OPTION."
echo -e "[1] Create an IoT Rule (S3) [2] Create DynamoDB table [3] Delete DynamoDB table [4] Run any API [5] Exit : \c"
read CHOICE

while [ "$CHOICE" -ne 5 ]; do
  if [ "$CHOICE" -eq 1 ]; then
    echo '<< Create an IoT Rule >>'
    echo ""
    sleep 0.5s

    # ask if template should be modified
    echo -e "Do you want to modify CloudFormation Template (Y/N) : \c"
    read MODIFY_CHOICE

    # regular expression for number
    re='^[0-9]+$'

    if [ "$MODIFY_CHOICE" = "Y" ]; then
      # modify template
      echo '<< Modify CloudFormation Template for IoT Rule >>'
      # 1. Get parameters from STDIN 
      echo -e "Enter IoT Rule Name (type 1 to skip): \c"
      read rn
      # if [[ "$rn" =~ $re ]]; then
      RULE_NAME=".Resources.MyTopicRule.Properties.RuleName=\""$rn"\""
      # fi

      echo -e "Enter sql query for this IoT Rule (type 1 to skip): \c"
      read sql # "SELECT * FROM 'CarVi/test/+/+/+'"
      # if [[ "$sq;" =~ $re ]]; then
      SQL=".Resources.MyTopicRule.Properties.TopicRulePayload.Sql=\"$sql\""
      # fi

      echo -e "Enter S3 Bucket name as an action (type 1 to skip): \c"
      read bucket_name
      # if [[ "$bucket_name" =~ $re ]]; then
      BUCKET_NAME=".Resources.MyTopicRule.Properties.TopicRulePayload.Actions[0].S3.BucketName=\"$bucket_name\""
      # fi

      echo -e "S3 Bucket Key (type 1 to skip): \c"
      read key
      # if [[ "$key" =~ $re ]]; then
      KEY=".Resources.MyTopicRule.Properties.TopicRulePayload.Actions[0].S3.Key=$key"
      # fi

      echo User Input Successfully Received.. 
      sleep 1s
      echo Modifying CloudFormation Template......
      sleep 2s

      # # 2. Apply user input to CloudFormation Template (cf_iot_rule_gen_s3.json)

      # if ! [[ "$rn" =~ $re ]]; then
      echo `jq $RULE_NAME cf_iot_rule_gen_s3.json > tmp.$$.json && mv tmp.$$.json cf_iot_rule_gen_s3.json`
    # fi
    # if [[ "$sql" =~ $re ]]; then
      echo `jq "$SQL" cf_iot_rule_gen_s3.json > tmp.$$.json && mv tmp.$$.json cf_iot_rule_gen_s3.json`
    # fi
    # if [[ "$bucket_name" =~ $re ]]; then
      echo `jq $BUCKET_NAME cf_iot_rule_gen_s3.json > tmp.$$.json && mv tmp.$$.json cf_iot_rule_gen_s3.json`
    # fi
    # if [[ "$key" =~ $re ]]; then
      echo `jq $KEY cf_iot_rule_gen_s3.json > tmp.$$.json && mv tmp.$$.json cf_iot_rule_gen_s3.json`
    # fi

      echo CloudFormation Template is modified.
      sleep 1s
      echo Deploying Chalice......
      sleep 2s
      prev_path="cd .."
      eval $prev_path

      # deploy chalice and move to chalicelib folder
      echo `chalice deploy --no-autogen-policy`
      new_path="cd chalicelib"
      eval $new_path

      echo -e "[Enter to Process] \c" 
      read response
      # directly create an IoT Rule
      echo IoT Rule creating.....
      sleep 2s
      echo `http https://08448gkwdg.execute-api.us-west-2.amazonaws.com/api/iot/rule/create`
      echo ""
      echo IoT Rule is created.
      echo ""
      echo "SELECT THE OPTION."
      echo -e "[1] Create an IoT Rule (S3) [2] Create DynamoDB table [3] Delete DynamoDB table [4] Run any API [5] Exit : \c"
      read CHOICE
    else
      # skip the cloudformation template part, simply make a IoT rule
      echo -e "[Enter to Process] \c" 
      read response
      # directly create an IoT Rule
      echo IoT Rule creating.....
      sleep 2s
      echo `http https://08448gkwdg.execute-api.us-west-2.amazonaws.com/api/iot/rule/create`
      echo ""
      echo IoT Rule is created.
      echo ""
      echo "SELECT THE OPTION."
      echo -e "[1] Create an IoT Rule (S3) [2] Create DynamoDB table [3] Delete DynamoDB table [4] Run any API [5] Exit : \c"
      read CHOICE
    fi
  elif [ "$CHOICE" -eq 2 ]; then
    echo '<< Create a DynamoDB Table. >>'
    echo -e "Type API url to run : \c"
    read COMMAND    

    # # 3. Run chalice command to deploy template
    eval $COMMAND
    echo DynamoDB Table is Created.
    echo ""
    echo "SELECT THE OPTION."
    echo -e "[1] Create an IoT Rule (S3) [2] Create DynamoDB table [3] Delete DynamoDB table [4] Run any API [5] Exit : \c"
    read CHOICE
  elif [ "$CHOICE" -eq 3 ]; then
    echo '<< Delete a DynamoDB Table. >>'
    echo -e "Type API url to run : \c"
    read COMMAND    

    # # 3. Run chalice command to deploy template
    eval $COMMAND
    echo DynamoDB Table is deleted.
    echo ""
    echo "SELECT THE OPTION."
    echo -e "[1] Create an IoT Rule (S3) [2] Create DynamoDB table [3] Delete DynamoDB table [4] Run any API [5] Exit : \c"
    read CHOICE 
  elif [ "$CHOICE" -eq 4 ]; then
    echo '<< ANYTHING (for testing purpose) >>'
    echo -e "Type any API url to run : \c"
    read COMMAND    

    # # 3. Run chalice command to deploy template
    eval $COMMAND
    echo "$COMMAND" is executed. 
    echo ""
    echo "SELECT THE OPTION."
    echo -e "[1] Create an IoT Rule (S3) [2] Create DynamoDB table [3] Delete DynamoDB table [4] Run any API [5] Exit : \c"
    read CHOICE
  elif [ "$CHOICE" -eq 5 ]; then
    echo Terminating the program.... Thanks.
    exit 1
  fi
done


