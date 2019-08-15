import React from "react";
import { Image } from "react-native";
import { View, Text, TouchableOpacity } from "react-native";
import { createBottomTabNavigator, createStackNavigator} from "react-navigation";
import Search from "../screens/Tabs/Search";
import Category from "../screens/Tabs/Caregory";
import Like from "../screens/Tabs/Like";
import Profile from "../screens/Tabs/Profile";
import NavIcon from "../components/NavIcon";
import { Platform } from "react-native";
import {Feather} from "@expo/vector-icons";
import Camera from "../screens/Camera";
import styles from "../styles";

const stackFactory = (initialRoute, customConfig) =>
  createStackNavigator({
    InitialRoute: {
      screen: initialRoute,
      navigationOptions: {     
				headerStyle: {
					backgroundColor: styles.green,
					borderBottomWidth: 0 //헤더 밑의 줄 제거
				},...customConfig }
    }
  });


export default createBottomTabNavigator({
	Search: {
		screen: stackFactory(Search, {
			title: "Search",
		  	headerTitle: (
				<Image
					style={{height:35}}
					resizeMode = "contain"
					source={require("../assets/BeginVegan.png")}
				/>
		  	)
		//   headerRight: (
		// 	<TouchableOpacity>
		// 	  <Text>sss</Text>
		// 	</TouchableOpacity>
		//   )
		}),
		navigationOptions: {
        	tabBarIcon: (
          	<NavIcon name={Platform.OS === "ios" ? "ios-search" : "md-search"} />
        	)
      	}
	  },
	Category:{
		screen: stackFactory(Category, {
		  title: "Category"

		}),
		navigationOptions: {
        	tabBarIcon: (
          	<Feather name={"grid"} size= {26} />
        	)
      	}
	  },
	C: {
		screen: View,
		navigationOptions: {
			tabBarOnPress: ({navigation}) => navigation.navigate("Camera"),
			tabBarIcon: (
				<NavIcon name={Platform.OS === "ios" ? "ios-camera" : "md-camera"} />
			  )
			
		}
	},

	Like: {
		screen: stackFactory(Like, {
		  title: "Like"
		}),
		navigationOptions: {
        	tabBarIcon: (
          	<NavIcon name={Platform.OS === "ios" ? "ios-heart-empty" : "md-heart-empty"} />
        	)
      	}
	  },
	
	Profile: {
		screen: stackFactory(Profile, {
		  title: "Profile"
		}),
		navigationOptions: {
        	tabBarIcon: (
				<NavIcon name={Platform.OS === "ios" ? "ios-person" : "md-person"} />
        	)
      	}
	  }
	
},
{
	tabBarOptions:{
		showLabel: false,
		style: {
			backgroundColor: styles.green,
		}
	}
}
);

//홈화면