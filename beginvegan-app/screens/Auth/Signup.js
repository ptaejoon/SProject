import React, { useState } from "react";
import styled from "styled-components";
import AuthButton from "../../components/AuthButton";
import * as Facebook from 'expo-facebook';
import { TouchableOpacity } from "react-native-gesture-handler";

const View = styled.View`
  justify-content: center;
  align-items: center;
  flex: 1;
`;

const Text = styled.Text``;

const FBContainer = styled.View`
  margin-top: 25px;
  padding-top: 25px;
  border-style: solid;
`;


export default ({ navigation }) => {
  const [loading, setLoading] = useState(false);

  const fbLogin = async () => {
    try {
      const { type, token } = await Facebook.logInWithReadPermissionsAsync(
        "518422882047974",
        {
          permissions: ["public_profile"]
        }
      );
      if (type === "success") {
        const response = await fetch(
          `https://graph.facebook.com/me?access_token=${token}`
        );
        Alert.alert("Logged in!", `Hi ${(await response.json()).name}!`);
      } else {
        // type === 'cancel'
      }
    } catch ({ message }) {
      alert(`Facebook Login Error: ${message}`);
    }
  };
  


  return (
    <View>
          <FBContainer>
            <TouchableOpacity onPress={fbLogin}>
              <Text>{"sign up with facebook"}</Text>
            </TouchableOpacity>
          </FBContainer>
        </View>
  );
};
