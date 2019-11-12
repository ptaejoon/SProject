import React, { Component } from 'react';
import { FlatList, StyleSheet, Text, View ,Image, ScrollView} from 'react-native';
import constants from "../../constants";
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import { faSeedling, faCheese, faEgg, faFish, faDrumstickBite, faBacon, faLessThanEqual  } from '@fortawesome/free-solid-svg-icons';
import {Ionicons, Entypo} from "@expo/vector-icons";
import axios from "axios";

export default class FlatListBasics extends Component {

  state = {
    data: [],
    vegflag: false,
    milkflag: false,
    eggflag: false,
    fishflag: false,
    chickenflag: false,
    meatflag: false,
    imgurl: 'https://ak8.picdn.net/shutterstock/videos/1009250978/thumb/1.jpg',
    materails: '',
  };

  constructor(props){
    super(props)
    this.getData()
  }

  getData = async ()=>{
    await axios.get("http://localhost:8000/BeginVegan/productSpec/?title="+this.props.name)  
    .then(resp=>{
      this.setState({data: resp.data})

    })  
    .catch(error=>{
      console.log("error")
    });
    await this.setState({imgurl: this.state.data.Img[0].image})
    var i=0;
    for(i=0;i<this.state.data.Mat.length;i++){
      if(this.state.data.Mat[i].material.vcategory==="육류"){
        this.setState({meatflag: true})
      }
      if(this.state.data.Mat[i].material.vcategory==="가금류"){
        this.setState({chickenflag: true})
      }
      if(this.state.data.Mat[i].material.vcategory==="수산물"){
        this.setState({fishflag: true})
      }
      if(this.state.data.Mat[i].material.vcategory==="알"){
        this.setState({eggflag: true})
      }
      if(this.state.data.Mat[i].material.vcategory==="우유"){
        this.setState({milkflag: true})
      }
      if(this.state.data.Mat[i].material.vcategory==="식물"){
        this.setState({vegflag: true})
      }
      
      this.setState(current => (typeof current.materials == 'undefined' ? {materials: this.state.data.Mat[i].material.name} : {materials: current.materials+', '+this.state.data.Mat[i].material.name}));
      console.log(this.state.data.Mat[i].material.name)
    }
    console.log(this.state.materials)
  }

  render() {
    return (
      <ScrollView>
      <View style={styles.container}>
        <View style={styles.imagecontainer}>
        <Image 
          source={{uri: this.state.imgurl}}
          //source={{uri: "https://beginveganscrapdata.s3.ap-northeast-2.amazonaws.com/pd_img/[삼양라면]라면의 원조 컵 불닭볶음면 70g30개, 신세계적 쇼핑포털 SSG.COM.jpg"}}
          style={styles.image}
          ></Image>
        </View>

        <View style={styles.textContainer}>
          <Text style={styles.text}>{this.props.name}</Text>
        </View>

        <View style={styles.veganContainer}>
          {this.state.vegflag ?
          <FontAwesomeIcon icon={faSeedling} color="green" size={40}/> :
          <FontAwesomeIcon icon={faSeedling} color="red" size={40}/>
          }
          {
          this.state.milkflag ?
          <FontAwesomeIcon icon={faCheese} color="green" size={40}/> :
          <FontAwesomeIcon icon={faCheese} color="red" size={40}/>
          }
          {
          this.state.eggflag ?
          <FontAwesomeIcon icon={faEgg} color="green" size= {40} /> :
          <FontAwesomeIcon icon={faEgg} color="red" size= {40} />
          }
          {
          this.state.fishflag ?
          <FontAwesomeIcon icon={faFish} color="green" size= {40} /> :
          <FontAwesomeIcon icon={faFish} color="red" size= {40} />
          }
          {
          this.state.chickenflag ?
          <FontAwesomeIcon icon={faDrumstickBite} color="green" size= {40} /> :
          <FontAwesomeIcon icon={faDrumstickBite} color="red" size= {40} />
          }
          {
          this.state.meatflag ?
          <FontAwesomeIcon icon={faBacon} color="green" size= {40} /> :
          <FontAwesomeIcon icon={faBacon} color="red" size= {40} />
          }

        </View>
        <View style={styles.matContainer}>
          <Text style={{fontSize:20}}> 원재료 </Text>
          <Text style={{fontSize:14}}>{this.state.materials}</Text>

        </View>





      </View>
      </ScrollView>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "white",
    flex: 1,
    flexDirection: 'column',
    alignItems: 'center',
    paddingTop:15,

  },
  imageContainer: {
    width: constants.width,
    height: constants.height*(1/3),
    justifyContent: 'center',
    alignItems: 'center'
  },
  image: {
    height: 250,
    width: 200
  },
  textContainer:{
    backgroundColor: "white",
    width: constants.width,
    height: constants.height*(1/9),
    justifyContent: 'center',
    alignItems: 'center'    
  },
  text:{
    fontSize: 20
  },
  veganContainer:{
    backgroundColor: "white",
    width: constants.width,
    height: constants.height*(1/7),
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 30,
    flexDirection: 'row',
  },

  matContainer:{
    backgroundColor: "white",
    width: constants.width,
    height: constants.height*(1/5),
    justifyContent: 'flex-start',
    alignItems: 'flex-start' ,
    paddingRight:15,
    paddingLeft:15,
  }
  
})
