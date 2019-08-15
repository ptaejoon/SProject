import { createStackNavigator, createAppContainer } from "react-navigation";
import TabNavigation from "./TabNavigation";
import CameraNavigation from "./CameraNavigation";
import SearchNavigation from "./SearchNavigation";

const MainNavigation = createStackNavigator(
  {
    TabNavigation,
    CameraNavigation,
    SearchNavigation
  },
  {
    headerMode: "none",
    mode: "modal"
  }
);



export default createAppContainer(MainNavigation);

//가장 바닥의 stackNavigator