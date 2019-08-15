import { createStackNavigator, createAppContainer } from "react-navigation";
import Login from "../screens/Auth/Login";
import Signup from "../screens/Auth/Signup";
import AuthHome from "../screens/Auth/AuthHome";

const AuthNavigation = createStackNavigator(
  {
    AuthHome,
    Login,
    Signup
  },
  {
    headerMode: "none"
  }
);

export default createAppContainer(AuthNavigation);

//로그아웃 상태 초기화면