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

    const fieldTypes = Object.keys(dataTypes)

    const [fieldRows, setFieldRows] = useState<Array<FieldRow>>([
        {
            id: 1,
            fieldName: "",
            fieldType: fieldTypes[0],
        }
    ])

    return (
        <div id="sub-view">
            <p>Define your relation here:</p>
            <div className="columns">
                {
                    fieldRows.map(fieldRow => (
                        <FieldRowView
                            id={fieldRow.id}
                            fieldName={fieldRow.fieldName}
                            fieldType={fieldRow.fieldType}
                            onFieldNameEdit={handleFieldNameEdit}
                            onFieldTypeEdit={handleFieldTypeEdit}
                            onFieldAddition={handleFieldRowAddition}
                            onFieldDeletion={handleFieldRowDeletion}
                            showDelete={fieldRows.length > 1}
                            dataTypes={fieldTypes}
                            key={fieldRow.id}
                        />
                    ))
                }
            </div>
        </div>
    )

    function handleFieldRowAddition(id: number) {
        let _fieldRows = [...fieldRows]
        let idx = _fieldRows.findIndex(fieldRow => fieldRow.id === id)
        let newId = _fieldRows.length + 1
        let newRow: FieldRow = {
            fieldName: "",
            fieldType: fieldTypes[0],
            id: newId
        }
        _fieldRows.splice(idx + 1, 0, newRow)
        setFieldRows(_fieldRows)
    }


    function handleFieldRowDeletion(id: number) {
        let _fieldRows = [...fieldRows]
        let idx = _fieldRows.findIndex(fieldRow => fieldRow.id === id)
        _fieldRows.splice(idx, 1)
        setFieldRows(_fieldRows)
    }

    function handleFieldNameEdit(id: number, fieldName: string) {
        let _fieldRows = [...fieldRows]
        let idx = _fieldRows.findIndex(fieldRow => fieldRow.id === id)
        _fieldRows[idx].fieldName = fieldName

        setFieldRows(_fieldRows)

        console.table(_fieldRows)
    }

    function handleFieldTypeEdit(id: number, fieldType: string) {
        let _fieldRows = [...fieldRows]
        let idx = _fieldRows.findIndex(fieldRow => fieldRow.id === id)
        _fieldRows[idx].fieldType = fieldType

        setFieldRows(_fieldRows)

        console.table(_fieldRows)
    }
}

export default EditView