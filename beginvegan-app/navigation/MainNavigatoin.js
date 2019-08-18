import { createStackNavigator, createAppContainer } from "react-navigation";
import TabNavigation from "./TabNavigation";
import CameraNavigation from "./CameraNavigation";

const MainNavigation = createStackNavigator(
  {
    TabNavigation,
    CameraNavigation,
  },
  {
    headerMode: "none",
    mode: "modal"
  }
);



export default createAppContainer(MainNavigation);

//가장 바닥의 stackNavigator