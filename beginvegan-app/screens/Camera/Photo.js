import React, { Component } from 'react';
import { FlatList, StyleSheet, Text, View ,Image, ScrollView} from 'react-native';
import constants from "../../constants";
import { white } from "ansi-colors";

import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import { faSeedling, faCheese, faEgg, faFish, faDrumstickBite, faBacon, faLessThanEqual  } from '@fortawesome/free-solid-svg-icons';
import {Ionicons, Entypo} from "@expo/vector-icons";
import axios from "axios";
import custom from "../../styles";



export default class FlatListBasics extends Component {

  state = {
    data: [],
    vegflag: true,
    milkflag: true,
    eggflag: false,
    fishflag: false,
    chickenflag: true,
    meatflag: true,
    imgurl: 'https://ak8.picdn.net/shutterstock/videos/1009250978/thumb/1.jpg',
    materails: '소갈비, 소고기, 무, 대파, 쇠고기육수, 정제소금, 마늘, L-글루탐산나트륨, 국간장, 후추, 양파, 생강, 고추씨, 감초, 연잎, 진피, 오가피, 우유, 대두, 밀, 쇠고기, 닭고기',
  };

  constructor(props){
    super(props)
  }

  render() {
    return (
//      <ScrollView>
          <View style={styles.screensize}>
      <View style={styles.container}>
        <View style={styles.imagecontainer}>
        <Image 
 //         source={{uri: this.state.imgurl}}
          //source={{uri: "https://beginveganscrapdata.s3.ap-northeast-2.amazonaws.com/pd_img/[삼양라면]라면의 원조 컵 불닭볶음면 70g30개, 신세계적 쇼핑포털 SSG.COM.jpg"}}
         style={styles.image}
            source={{uri:"http://blogfiles.naver.net/MjAxOTA3MTNfMTU2/MDAxNTYzMDE5Nzk1ODQ3.2aoX0a0GC2sQrIGGjGFIsIRnuuWwJnJmNpGCFzuWEskg.74YmogrHAgIw6XcirrZ6oXbv0wYr30Rom9WAzSBZbEMg.JPEG.megaeagel9523/%EA%B3%A0%EC%98%81%EC%88%99_%EA%B0%88%EB%B9%84%ED%83%95_%EC%9B%90%EC%9E%AC%EB%A3%8C%EB%AA%85_%EB%B0%8F_%ED%95%A8%EB%9F%89.JPG"}}
          ></Image>
        </View>


        <View style={styles.veganContainer}>
          {this.state.vegflag ?
          <FontAwesomeIcon icon={faSeedling} color="green" size={30}/> :
          <FontAwesomeIcon icon={faSeedling} color="grey" size={30}/>
          }
          {
          this.state.milkflag ?
          <FontAwesomeIcon icon={faCheese} color="green" size={30}/> :
          <FontAwesomeIcon icon={faCheese} color="grey" size={30}/>
          }
          {
          this.state.eggflag ?
          <FontAwesomeIcon icon={faEgg} color="green" size= {30} /> :
          <FontAwesomeIcon icon={faEgg} color="grey" size= {30} />
          }
          {
          this.state.fishflag ?
          <FontAwesomeIcon icon={faFish} color="green" size= {30} /> :
          <FontAwesomeIcon icon={faFish} color="grey" size= {30} />
          }
          {
          this.state.chickenflag ?
          <FontAwesomeIcon icon={faDrumstickBite} color="green" size= {30} /> :
          <FontAwesomeIcon icon={faDrumstickBite} color="grey" size= {30} />
          }
          {
          this.state.meatflag ?
          <FontAwesomeIcon icon={faBacon} color="green" size= {30} /> :
          <FontAwesomeIcon icon={faBacon} color="grey" size= {30} />
          }

        </View>

        <View style={styles.splitContainer}>

        <View style={styles.matContainer}>
            <Text style={{fontSize:30, fontFamily: 'Ys', width: constants.width/2,}}> 원재료 </Text>
            <Text style={{fontSize:14, fontFamily: 'Ys', width: constants.width/2,}}>소갈비, 소고기, 무, 대파, 쇠고기육수, 정제소금, 마늘, L-글루탐산나트륨, 국간장, 후추, 양파, 생강, 고추씨, 감초, 연잎, 진피, 오가피, 우유, 대두, 밀, 쇠고기, 닭고기</Text>
          </View>


          <View style={{backgroundColor:"white", flex:0.5, paddingTop: 15, justifyContent:"center"}}>
          <View style={{backgroundColor:'white', justifyContent:'center', alignContent:'center', alignItems :'center', width: constants.width/2,}}>
            <Text style={{backgroundColor:'white',color:"red", fontSize:20, fontFamily: 'Ys'}}> 조인성님에게 부적합 </Text>
          </View>
          {/* <View style={styles.starContainer}>

            <Ionicons name={"ios-star-outline"} color={"black"} size={30}/> 
            <Ionicons name={"ios-star-outline"} color={"black"} size={30}/> 
            <Ionicons name={"ios-star-outline"} color={"black"} size={30}/> 
            <Ionicons name={"ios-star-outline"} color={"black"} size={30}/> 
            <Ionicons name={"ios-star-outline"} color={"black"} size={30}/> 

          </View>           */}
          </View>

        </View>



      </View>
          </View>
//      </ScrollView>
    );
  }
}

const styles = StyleSheet.create({

  screensize: {
    backgroundColor:"white",
    padding: 15,
    width: constants.width,
    height: constants.height *(3/4)
  },

  container: {
    backgroundColor: "white",
    flex: 1,
    flexDirection: 'column',
    alignItems: 'center',
//    paddingTop:15,
//    borderRadius: 50,
  },
  imageContainer: {
//    width: constants.width,
//    height: constants.height*(1/3),
    justifyContent: 'center',
    alignItems: 'center',
//    flex: 0.5,
//    borderRadius: 50,
  },
  image: {
    alignSelf: "center",
    resizeMode: "contain",
    height: constants.height*(3/4)*0.4,
    width: constants.width*0.8,
    borderRadius: 50,
  },
  textContainer:{
    backgroundColor: "white",
    width: constants.width,
    height: constants.height*(1/9),
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: "white",
  },
  text:{
    fontSize: 35,
    fontFamily: 'Ys'
  },
  veganContainer:{
    backgroundColor: "white",
    width: constants.width,
    height: constants.height*(1/7),
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 30,
    flexDirection: 'row',
    borderRadius: 30,
  },

  starContainer:{
    backgroundColor: "white",
    width: constants.width/2,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 30,
    flexDirection: 'row',
    borderRadius: 30,
  },

  matContainer:{
    backgroundColor: "white",
    width: constants.width/2,
    height: constants.height*(1/5),
    justifyContent: 'flex-start',
    paddingRight:5,
    paddingLeft:5,
    paddingTop:15,
  },

  splitContainer:{
    backgroundColor: "white",
    width: constants.width,
 //   flex: 3,
    flexDirection: 'row',
//    alignItems: 'center',
//   justifyContent: "flex-end"
  }
  
})
