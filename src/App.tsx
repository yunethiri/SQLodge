
import './App.scss'
import TableView from './components/TableView'
import EditView from './components/EditView'
import { useState } from 'react'

export interface RelationView {
  columns: Array<string>
  rows: Array<{ [key: string]: any }> // ? represents the string-key, arbitrary-value type, for example [{"id": 2, "name": "mehdi"}, {"id": 1, "name": "fuad"}]}
}

function App() {

  const [currentRelationView, setCurrentRelationView] = useState<RelationView>({
    columns: [],
    rows: []
  })

  return (
    <div className="App">
      <div id="main-view">
        <EditView relationView={currentRelationView} onRelationChange={handleRelationViewUpdate} />
        <TableView relationView={currentRelationView} />
      </div>
    </div>
  )

  function handleRelationViewUpdate(relationView: RelationView) {
    setCurrentRelationView(relationView)
  }
}

export default App
