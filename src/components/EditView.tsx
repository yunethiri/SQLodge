import React, { useState } from "react"
import FieldRowView from "./FieldRowView"
import * as api from '../api'
import { RelationView } from "../App"

export type StringMap = { [dtype: string]: string }

interface FieldRow {
    id: number
    fieldName: string
    fieldType: string
}

interface EditViewProps {
    relationView: RelationView
    onRelationChange: (relationView: RelationView) => void
}


const EditView = (props: EditViewProps) => {
    const dataTypes: StringMap = {
        'boolean': 'BOOL',
        'integer': 'INT',
        'text': 'TEXT',
        'time': 'TIME',
    }

    const fieldTypes = Object.keys(dataTypes)

    const [showDefinitionField, setShowDefinitionField] = useState<boolean>(true)


    const [fieldRows, setFieldRows] = useState<Array<FieldRow>>([
        {
            id: 1,
            fieldName: "",
            fieldType: fieldTypes[0],
        }
    ])
    const [relationName, setRelationName] = useState<string>("")
    const [insertionValues, setInsertionValues] = useState<StringMap>({})
    const [updateValues, setUpdateValues] = useState<StringMap>({})

    return (
        <div id="sub-view">
            {
                showDefinitionField &&
                <div className="relation-definition">
                    <p>Define your relation here:</p>
                    <div className="relation-name">
                        <p>Relation name:&nbsp;</p>
                        <input type="text" value={relationName} onChange={handleRelationNameChange} />
                    </div>
                    <div className="field-rows">
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
                    <div className="create-relation-button">
                        <button onClick={hanldeRelationCreation}>Create Relation</button>
                    </div>
                </div>
            }
            {
                !showDefinitionField &&
                <div className="relation-edition">
                    <div className="value-insertion">
                        <p>Use the below fields to insert an entry:</p>
                        {
                            props.relationView.columns.map(col => {
                                if (col !== "id") {
                                    return (
                                        <div className="row-value" key={col}>
                                            <p>{col}:&nbsp;</p>
                                            <input
                                                type="text"
                                                value={insertionValues[col]}
                                                onChange={(event) => {
                                                    handleInsertionValueEdit(event, col)
                                                }}
                                            />
                                        </div>
                                    )
                                }
                            })
                        }
                        <button onClick={handleEntryInsertion}>Insert Entry</button>
                    </div>
                    <div className="value-modification">
                        <p>Use the below fields to modify an existing entry:</p>
                        {
                            props.relationView.columns.map(col => {
                                return (
                                    <div className="row-value" key={col}>
                                        <p>{col}:&nbsp;</p>
                                        <input
                                            type="text"
                                            value={updateValues[col]}
                                            onChange={(event) => {
                                                handleUpdateValueEdit(event, col)
                                            }}
                                        />
                                    </div>
                                )
                            })
                        }
                        <button onClick={handleEntryUpdate}>Update Entry</button>
                    </div>
                    <div className="value-deletion">
                        <p>Insert the row id to be removed from the relation: </p>
                        <div>
                            <input type="text" />
                            <button>Remove</button>
                        </div>
                    </div>
                </div>
            }
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
    }

    function handleFieldTypeEdit(id: number, fieldType: string) {
        let _fieldRows = [...fieldRows]
        let idx = _fieldRows.findIndex(fieldRow => fieldRow.id === id)
        _fieldRows[idx].fieldType = fieldType

        setFieldRows(_fieldRows)

    }

    function handleRelationNameChange(event: React.ChangeEvent<HTMLInputElement>) {
        setRelationName(event.target.value)
    }

    function handleInsertionValueEdit(event: React.ChangeEvent<HTMLInputElement>, col: string) {
        let _insertionValues = { ...insertionValues }
        _insertionValues[col] = event.target.value
        setInsertionValues(_insertionValues)
    }

    function handleUpdateValueEdit(event: React.ChangeEvent<HTMLInputElement>, col: string) {
        let _updateValues = { ...updateValues }
        _updateValues[col] = event.target.value
        setUpdateValues(_updateValues)
    }

    async function hanldeRelationCreation() {
        let body: { [name: string]: string } = {}

        fieldRows.forEach(fieldRow => {
            if (fieldRow.fieldName === "") {
                fieldRow.fieldName = "no_name"
            }
            body[fieldRow.fieldName] = dataTypes[fieldRow.fieldType]
        }
        )

        let relation = {
            name: relationName,
            body: body
        }

        await api.createRelation(relation)

        let submittedRelation = await api.getRelation(relationName)

        //? Updating states for edit and add fields
        let _insertionValues: StringMap = {}
        let _updateValues: StringMap = {}
        submittedRelation.columns.forEach(col => {
            if (col !== "id")
                _insertionValues[col] = ""

            _updateValues[col] = ""
        })
        setInsertionValues(_insertionValues)
        setUpdateValues(_updateValues)


        props.onRelationChange(submittedRelation)
        setShowDefinitionField(false)
    }

    async function handleEntryInsertion() {
        let insertionData = {
            name: relationName,
            body: insertionValues
        }
        await api.insertEntry(insertionData)
        let latestRelation = await api.getRelation(relationName)
        props.onRelationChange(latestRelation)
    }

    async function handleEntryUpdate() {
        let updateData = {
            name: relationName,
            body: updateValues,
            id: updateValues.id
        }
        await api.updateEntry(updateData)
        let latestRelation = await api.getRelation(relationName)
        props.onRelationChange(latestRelation)
    }


}

export default EditView