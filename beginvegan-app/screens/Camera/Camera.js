import React, { useState, useEffect, useRef } from "react";
import styled from "styled-components";
import { Camera } from "expo-camera";
import * as MediaLibrary from "expo-media-library";
import constants from "../../constants";
import Loader from "../../components/Loader";
import * as Permissions from "expo-permissions";
import { Ionicons } from "@expo/vector-icons";
import { TouchableOpacity, Platform } from "react-native";
import styles from "../../styles";
import axios from "axios";

const View = styled.View`
  flex: 1;
  justify-content: center;  
  align-items: center;
  backgroundColor: ${styles.green};
`;

const Icon = styled.View``;

const Button = styled.View`
  width: 80;
  height: 80;
  border-radius: 40px;
  border: 10px solid lightgrey;
  
`;


export default ({ navigation }) => {
  const cameraRef = useRef();
  const [canTakePhoto, setCanTakePhoto] = useState(true);
  const [loading, setLoading] = useState(true);
  const [hasPermission, setHasPermission] = useState(false);
  const [cameraType, setCameraType] = useState(Camera.Constants.Type.back);
  const takePhoto = async () => {
    if (!canTakePhoto) {
      return;
    }
    try {
//      console.log(cameraRef.current)
      setCanTakePhoto(false);
      const { uri } = await cameraRef.current.takePictureAsync({
        quality: 1
      });
      console.log(uri)
 //     const asset = await MediaLibrary.createAssetAsync(uri);
 //     console.log(asset);

      const formData = new FormData()
      formData.append("img", uri)
      axios.post("http://tj-rest-server-dev.ap-northeast-2.elasticbeanstalk.com/BeginVegan/materials/", formData, {
        headers: {
          "content-type": "multipart/form-data"
        }
      })
      .then(function (response) {
        //handle success
        console.log(response);
    })
    .catch(function (response) {
        //handle error
        console.log(response);
    });
    } catch (e) {
      console.log(e);
      setCanTakePhoto(true);
    }
  };

  const askPermission = async () => {
    try {
      const { status } = await Permissions.askAsync(Permissions.CAMERA);
      if (status === "granted") {
        setHasPermission(true);
 //       console.log("okokokok")
      }
    } catch (e) {
      console.log(e);
      setHasPermission(false);
    } finally {
      setLoading(false);
    }
  };
  const toggleType = () => {
    if (cameraType === Camera.Constants.Type.front) {
      setCameraType(Camera.Constants.Type.back);
    } else {
      setCameraType(Camera.Constants.Type.front);
    }
  };
  useEffect(() => {
    askPermission();
  }, []);


  
  return (
    <View>
      {loading ? (
        <Loader />
      ) : hasPermission ? (
        <>
          <Camera
            ref={cameraRef}
            type={cameraType}
            style={{
              justifyContent: "flex-end",
              padding: 15,
              width: constants.width,
              height: constants.height *(3/4)
            }}
          >
            <TouchableOpacity onPress={toggleType}>
              <Icon>
                <Ionicons
                  name={
                    Platform.OS === "ios"
                      ? "ios-reverse-camera"
                      : "md-reverse-camera"
                  }
                  size={32}
                  color={"white"}
                />
              </Icon>
            </TouchableOpacity>
          </Camera>
          <View>
            <TouchableOpacity onPress={takePhoto} disabled={!canTakePhoto}>
              <Button />
            </TouchableOpacity>
          </View>
        </>
      ) : null}
    </View>
  );
};