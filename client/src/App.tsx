import React from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from "react-router-dom";
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Drawer from '@mui/material/Drawer';
import { createTheme, ThemeProvider} from '@mui/material/styles';

import socket from './utils/websocket';
import RealtTime from './pages/Realtime';
import Scenarios from './pages/Scenarios';
import Home from './pages/home';

socket.on('connection', () => {
    console.log("connected");
  }
)

const App = () => {

  const theme = createTheme({
    palette: {
      mode: 'dark',
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Box sx={{ display: 'flex'}}>
            <Drawer variant="permanent" anchor="left" sx={{ width: 200, flexShrink: 0, '& .MuiDrawer-paper': {width: 200}}}>
              <Toolbar>
                <Typography> ATC Simulator</Typography>
              </Toolbar>
              <Divider />
              <List>
                <ListItemButton component={Link} to='/'>
                  <ListItemText primary={"Dashboard"} />
                </ListItemButton>
                <ListItemButton component={Link} to='/realtime'>
                  <ListItemText primary={"Real Time Simulation"}/>
                </ListItemButton>
                <ListItemButton component={Link} to='/scenarios'>
                  <ListItemText primary={"Scenarios"}/>
                </ListItemButton>
              </List>
            </Drawer> 
          <Box component="main" sx={{ flexGrow: 1}}>
            <Switch>
              <Route path="/realtime" component={RealtTime}/>
              <Route path="/scenarios" component={Scenarios}/>
              <Route path="/" exact component={Home}/>
            </Switch>  
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
