
import './App.scss'
import TableView from './components/TableView'
import EditView from './components/EditView'

function App() {


  return (
    <div className="App">
      <div id="main-view">
        <EditView />
        <TableView />
      </div>
    </div>
  )
}

export default App
