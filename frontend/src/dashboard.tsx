import * as React from 'react';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import ListSubheader from '@mui/material/ListSubheader';
import IconButton from '@mui/material/IconButton';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import LanguageIcon from '@mui/icons-material/Language';
import DeleteIcon from '@mui/icons-material/Delete';
import AppBar from '@mui/material/AppBar';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import UploadIcon from '@mui/icons-material/Upload';
import Box from '@mui/material/Box';
import { Dialog, DialogTitle, DialogContent, DialogActions } from "@material-ui/core";
import axiosInstance from './api/axiosInstance';
import axios, { AxiosResponse, AxiosError } from 'axios';
import API_URL from './api/general';
import { makeStyles } from '@material-ui/core/styles';
import Fab from '@material-ui/core/Fab';
import Icon from '@material-ui/core/Icon';

const useStyles = makeStyles((theme) => ({
  fab: {
    position: 'fixed',
    bottom: theme.spacing(2),
    right: theme.spacing(2),
  },
  icon: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
  },
}));


export default function App(){
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [file, setFile] = React.useState<File | null>(null);
  const [images,setImages] = React.useState([]);


  React.useEffect(()=>{
    axiosInstance.get('/image/my-images',  {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    })
    .then((response: AxiosResponse) => {
      console.log(response.data)
      setImages(response.data)
    })
    .catch((error: AxiosError) => {
      console.error(error);
    });
  },[loading == false])

  const handleUpload = (e:any) => {
    if (file) {
      setLoading(true);
      const formData = new FormData();
      formData.append('file', file);
      axiosInstance.post(`/image/upload-image?thumbnail_size=128`, formData,  {
        headers: {
          'accept': 'application/json',
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      })
        .then((response) => {
          console.log(response.data);
          setLoading(false);
          handleClose();
        })
        .catch((error) => {
          console.error(error);
          setLoading(false);
          // setError('Error uploading image');
        });
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0])
    }
  }
  return(
    <>
    <Fab color="primary" aria-label="add" className={classes.fab}>
    <UploadIcon onClick={handleOpen}/>
    </Fab>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Image server
          </Typography>
          <Button color="inherit">Logout</Button>
        </Toolbar>
      </AppBar>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Upload File</DialogTitle>
        <DialogContent>
          <input type="file" accept="image/*" onChange={handleFileChange}/>
          {loading && <p>Loading...</p>}
          {error && <p>{error}</p>}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button color="primary" onClick={handleUpload}>
            Upload
          </Button>
        </DialogActions>
      </Dialog>
      <TitlebarImageList images={images}/>
    </>
    
  )
}
interface Images {
  user_id: number;
  id: number;
  image: string;
}

interface MyComponentProps {
  images: Images[];
}

function TitlebarImageList({ images }: MyComponentProps ) {
  return (
    <ImageList cols={5}>
    {images.map((item) => (
      <ImageListItem key={item.id} style={{cursor:'pointer'}} onClick={()=>console.log('haloo')}>
        <img
          src={`${API_URL}/image/${item.image}`}
          srcSet={`${API_URL}/image/${item.image}`}
          // alt={item.id}
          loading="lazy"
        />
        <ImageListItemBar
          subtitle={item.image.split('.').pop()}
          title={item.image.split('.').slice(0, -1).join('.')}
          actionIcon={
            <>
             <IconButton
              sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
              aria-label={`info about ${item.id}`}
              onClick={()=> window.open(`${API_URL}/image/${item.image}`, "_blank")}
            >
              <LanguageIcon />
            </IconButton>
            <IconButton
              sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
              aria-label={`info about ${item.id}`}
              onClick={()=>navigator.clipboard.writeText(`${API_URL}/image/${item.image}`)}
            >
              <ContentCopyIcon />
            </IconButton>
            <IconButton
              sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
              aria-label={`info about ${item.id}`}
              onClick={()=>alert('delte')}
            >
              <DeleteIcon />
            </IconButton>
            </>
           
          }
        />
      </ImageListItem>
    ))}
  </ImageList>
  
  );
}

const itemData = [
  {
    img: 'https://images.unsplash.com/photo-1551963831-b3b1ca40c98e',
    title: 'Breakfast',
    author: '@bkristastucchio',
    rows: 2,
    cols: 2,
    featured: true,
  },
  {
    img: 'https://images.unsplash.com/photo-1551782450-a2132b4ba21d',
    title: 'Burger',
    author: '@rollelflex_graphy726',
  },
  {
    img: 'https://images.unsplash.com/photo-1522770179533-24471fcdba45',
    title: 'Camera',
    author: '@helloimnik',
  },
  {
    img: 'https://images.unsplash.com/photo-1444418776041-9c7e33cc5a9c',
    title: 'Coffee',
    author: '@nolanissac',
    cols: 2,
  },
  {
    img: 'https://images.unsplash.com/photo-1533827432537-70133748f5c8',
    title: 'Hats',
    author: '@hjrc33',
    cols: 2,
  },
  {
    img: 'https://images.unsplash.com/photo-1558642452-9d2a7deb7f62',
    title: 'Honey',
    author: '@arwinneil',
    rows: 2,
    cols: 2,
    featured: true,
  },
  {
    img: 'https://images.unsplash.com/photo-1516802273409-68526ee1bdd6',
    title: 'Basketball',
    author: '@tjdragotta',
  },
  {
    img: 'https://images.unsplash.com/photo-1518756131217-31eb79b20e8f',
    title: 'Fern',
    author: '@katie_wasserman',
  },
  {
    img: 'https://images.unsplash.com/photo-1597645587822-e99fa5d45d25',
    title: 'Mushrooms',
    author: '@silverdalex',
    rows: 2,
    cols: 2,
  },
  {
    img: 'https://images.unsplash.com/photo-1567306301408-9b74779a11af',
    title: 'Tomato basil',
    author: '@shelleypauls',
  },
  {
    img: 'https://images.unsplash.com/photo-1471357674240-e1a485acb3e1',
    title: 'Sea star',
    author: '@peterlaster',
  },
  {
    img: 'https://images.unsplash.com/photo-1589118949245-7d38baf380d6',
    title: 'Bike',
    author: '@southside_customs',
    cols: 2,
  },
];