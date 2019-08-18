import React from "react";
import {createStackNavigator} from "react-navigation";
import Camera from "../screens/Camera";
import styles from "../styles";
import NavIcon from "../components/NavIcon";
import { Platform } from "react-native";
import {Text} from "react-native";



export default createStackNavigator(
  {
    Camera:{  
      screen: Camera,
      
      navigationOptions: {
        headerTitle: <Text style={{color:"white", fontSize:17}}>제품의 원재료명을 찍어주세요</Text>,
        headerMode: "float",
        headerStyle: {
					backgroundColor: styles.green,
          borderBottomWidth: 0, //헤더 밑의 줄 제거
				}
      }
    }
  },
  {
    navigationOptions: {
      headerMode: "float",
    }
  }
);
