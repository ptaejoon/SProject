import React from "react";
import styled from "styled-components";
import styles from "../../styles";

const View = styled.View`
  padding: 15,
  width: constants.width,
  height: constants.height *(3/4)
`;

const Text = styled.Text`
`;

export default () => (
  <View>
    <Text>Like</Text>

  </View>
);