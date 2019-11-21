import React, { Component } from 'react';
import { FlatList, StyleSheet, Text, View ,Image, ScrollView} from 'react-native';
import constants from "../../constants";
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import { faSeedling, faCheese, faEgg, faFish, faDrumstickBite, faBacon, faLessThanEqual  } from '@fortawesome/free-solid-svg-icons';
import {Ionicons, Entypo} from "@expo/vector-icons";
import axios from "axios";
import custom from "../../styles";
import { TouchableOpacity } from 'react-native-gesture-handler';

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
    star_idx: -1,
  };

  constructor(props){
    super(props)
    this.getData()
  }

  getData = async ()=>{
 //   await axios.get("http://localhost:8000/BeginVegan/productSpec/?title="+this.props.name)
    await axios.get("http://tj-rest-server-dev.ap-northeast-2.elasticbeanstalk.com/BeginVegan/productSpec/?title="+this.props.name)  
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
//      console.log(this.state.data.Mat[i].material.name)
    }
//    console.log(this.state.materials)
  }

  change_rating= (idx)=>{
    if(this.state.star_idx==idx)
      this.setState({star_idx:-1})
    else
      this.setState({star_idx:idx})
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
            <Text style={{fontSize:14, fontFamily: 'Ys', width: constants.width/2,}}>{this.state.materials}</Text>
          </View>


          <View style={{backgroundColor:"white", flex:0.5, paddingTop: 15, justifyContent:"center"}}>
          <View style={{backgroundColor:'white', justifyContent:'center', alignContent:'center', alignItems :'center', width: constants.width/2,}}>
            <Text style={{backgroundColor:'white',color:"green", fontSize:20, fontFamily: 'Ys'}}> 조인성님에게 적합 </Text>
          </View>
          <View style={styles.starContainer}>
            <TouchableOpacity onPress = {()=>this.change_rating(1)}>
              {this.state.star_idx >= 1 ? <Ionicons name={"ios-star-outline"} color={custom.green} size={30}/> : <Ionicons name={"ios-star-outline"} color={"black"} size={30}/>}
            </TouchableOpacity>
            <TouchableOpacity onPress = {()=>this.change_rating(2)}>
              {this.state.star_idx >= 2 ? <Ionicons name={"ios-star-outline"} color={custom.green} size={30}/> : <Ionicons name={"ios-star-outline"} color={"black"} size={30}/>} 
            </TouchableOpacity>
            <TouchableOpacity onPress = {()=>this.change_rating(3)}>
              {this.state.star_idx >= 3 ? <Ionicons name={"ios-star-outline"} color={custom.green} size={30}/> : <Ionicons name={"ios-star-outline"} color={"black"} size={30}/>} 
            </TouchableOpacity>
            <TouchableOpacity onPress = {()=>this.change_rating(4)}>
              {this.state.star_idx >= 4 ? <Ionicons name={"ios-star-outline"} color={custom.green} size={30}/> : <Ionicons name={"ios-star-outline"} color={"black"} size={30}/>} 
            </TouchableOpacity>
            <TouchableOpacity onPress = {()=>this.change_rating(5)}>
              {this.state.star_idx >= 5 ? <Ionicons name={"ios-star-outline"} color={custom.green} size={30}/> : <Ionicons name={"ios-star-outline"} color={"black"} size={30}/>}
            </TouchableOpacity> 

          </View>          
          </View>

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
//    paddingTop:15,
//    borderRadius: 50,
  },
  imageContainer: {
//    width: constants.width,
//    height: constants.height*(1/3),
    justifyContent: 'center',
    alignItems: 'center',
    flex: 0.5,
//    borderRadius: 50,
  },
  image: {
    height: 250,
    width: 200,
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
