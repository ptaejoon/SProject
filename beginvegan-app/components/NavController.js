import React from "react";
import { View } from "react-native";
import { useIsLoggedIn } from "../AuthContext";
import AuthNavigation from "../navigation/AuthNavigation";
import MainNavigation from "../navigation/MainNavigatoin";

export default () => {
  const isLoggedIn = true;
  return (
    <View style={{ flex: "1" }}>
      {/* {isLoggedIn ? <MainNavigation /> : <AuthNavigation />} */}
      <MainNavigation/>
    </View>
  );
};

//App.js.에서 navController 실행 로그인에 따라 화면 선택해준다.