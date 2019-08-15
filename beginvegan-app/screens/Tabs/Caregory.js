import React, { Component } from 'react';
import {  View, Text, FlatList, ScrollView ,Image} from 'react-native';
import styled from "styled-components";


// const View = styled.View`
//   justify-content: center;
//   align-items: center;
//   flex: 1;
// `;

// const Text = styled.Text``;

export default class Test extends Component {
    constructor(props) {
        super(props);

        this.state = {
            categories: [
                {
                    id: 1,
                    title: "cat1",
                    images: [
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        },
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        },
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        },
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        },
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        },{
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        },
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        }
                    ]
                },
                {
                    id: 2,
                    title: "cat2",
                    images: [
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        },
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        },
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        }
                    ]
                },
                {
                    id: 3,
                    title: "cat3",
                    images: [
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        },
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        },
                        {
                            image: "https://cdn.imweb.me/thumbnail/20190210/5c5fb18ebc39c.jpg",
                        }
                    ]
                }
            ]
        }
    }
   
    _renderItem = ({item}) => (
        <Image style={{width:100,height:100}}  source={{uri : item.image}}/>
      );

    _keyExtractor = (item, index) => index;
      
    render() {
        return (
            <ScrollView style={{ flex: 1}}>
                {this.state.categories.map((cat, index) => {
                    return (
                        <View key={cat.id}>
                        <Text>{cat.title}</Text>
                        <FlatList
                            data={cat.images}
                            numColumns={3}
                            extraData={cat.images}
                            keyExtractor={this._keyExtractor}
                            renderItem={this._renderItem}
                        />
                        </View>
                    )
                })}
            </ScrollView>
        );
    }
}