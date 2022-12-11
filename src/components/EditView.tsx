import { useState } from "react"
import FieldRow from "./FieldRow"

const EditView = () => {
    const [fieldRows, setFieldRows] = useState<Array<number>>([])
    const dataTypes = {
        'boolean': 'BOOL',
        'integer': 'INT',
        'text': 'TEXT',
        'time': 'TIME',
    }

    return (
        <div id="sub-view">
            <p>Define your relation here:</p>
            <div className="columns">
                <FieldRow
                    id={0}
                    showDelete={false}
                    dataTypes={Object.keys(dataTypes)}
                    onAddField={handleFieldRowAddition}
                />
            </div>
        </div>
    )

    function handleFieldRowAddition(id: number) {
        
    }
}

export default EditView