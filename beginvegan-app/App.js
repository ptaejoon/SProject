import React, { useState, useEffect } from "react";

import * as Font from 'expo-font'
import {Asset} from 'expo-asset'

import { Ionicons } from "@expo/vector-icons";
import { AppLoading } from "expo";
import { AsyncStorage } from "react-native";
import { InMemoryCache } from "apollo-cache-inmemory";
import { persistCache } from "apollo-cache-persist";
import ApolloClient from "apollo-boost";
import { ThemeProvider } from "styled-components";
import { ApolloProvider } from "react-apollo-hooks";
import apolloClientOptions from "./apollo";
import AuthNavigaton from "./navigation/AuthNavigation";
import styles from "./styles";
import NavController from "./components/NavController";
import { AuthProvider } from "./AuthContext";






export default function App() {
  const [loaded, setLoaded] = useState(false);
//  const [client, setClient] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(true);


  const preLoad = async () => {       //폰트 불러옴, 앱 필요이미지 등등
    try {
      await Font.loadAsync({
        ...Ionicons.font,
        Rancho: require('./assets/font/Rancho-Regular.ttf'),
        Ys: require('./assets/font/YeonSung-Regular.ttf')
      });


      // await Asset.loadAsync([require("./assets/BeginVegan.png")]);

      const cache = new InMemoryCache();
      await persistCache({
        cache,
        storage: AsyncStorage
      });


 //     const client = new ApolloClient({
 //       cache,
 //       ...apolloClientOptions
 //     });

      const isLoggedIn = await AsyncStorage.getItem("isLoggedIn");
      if (!isLoggedIn || isLoggedIn === "false") {
        setIsLoggedIn(true);
      } else {
        setIsLoggedIn(flase);
      }


      setLoaded(true);
//      setClient(client);


    } catch (e) {
      console.log(e);
    }
  };



  useEffect(() => {
    preLoad();
  }, []);



  return loaded /*&& client*/ && isLoggedIn !== null ? (
 //   <ApolloProvider client={client}>
      <ThemeProvider theme={styles}>
        <AuthProvider isLoggedIn={isLoggedIn}>
          <NavController />
        </AuthProvider>
      </ThemeProvider>
 //   </ApolloProvider>
  ) : (
    <AuthNavigaton /> //로그아웃 상태, 초기화면
  );
}
