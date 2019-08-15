import React from "react";
import {createStackNavigator} from "react-navigation";
import SearchResult from "../screens/SearchResult";




export default createStackNavigator(
  {
    SearchResult
  },
  {
    navigationOptions: {
      headerMode: "float",
    }
  }
);