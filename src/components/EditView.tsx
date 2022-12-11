import { useState } from "react"
import FieldRowView from "./FieldRowView"

interface FieldRow {
    id: number
    fieldName: string
    fieldType: string
}

const EditView = () => {
    const dataTypes = {
        'boolean': 'BOOL',
        'integer': 'INT',
        'text': 'TEXT',
        'time': 'TIME',
    }

    const [fieldRows, setFieldRows] = useState<Array<FieldRow>>([
        {
            id: 0,
            fieldName: "",
            fieldType: Object.keys(dataTypes)[0],
        }
    ])

    return (
        <div id="sub-view">
            <p>Define your relation here:</p>
            <div className="columns">
                {
                    fieldRows.map(fieldRow => (
                        <FieldRowView
                            key={fieldRow.id}
                            id={fieldRow.id}
                            showDelete={false}
                            dataTypes={Object.keys(dataTypes)}
                            onFieldAddition={handleFieldRowAddition}
                            onFieldUpdate={handleFieldUpdate}
                        />
                    ))
                }
            </div>
        </div>
    )

    function handleFieldRowAddition(id: number) {

    }

    function handleFieldUpdate(id: number, fieldName: string, fieldType: string) {
        let _fieldRows = [...fieldRows]
        let idx = _fieldRows.findIndex(fieldRow => fieldRow.id === id)
        if (idx !== null) {
            _fieldRows[idx].fieldName = fieldName
            _fieldRows[idx].fieldType = fieldType
        }
        setFieldRows(_fieldRows)
        console.table(_fieldRows)
    }
}

export default EditView