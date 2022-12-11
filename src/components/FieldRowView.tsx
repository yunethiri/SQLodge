import { useState } from "react"

interface FieldRowProps {
    showDelete: boolean
    id: number
    dataTypes: Array<string>
    onFieldAddition: (id: number) => void
    onFieldUpdate: (id: number, fieldName: string, fieldType: string) => void
}

const FieldRowView = (props: FieldRowProps) => {
    const [fieldName, setFieldName] = useState<string>("")
    const [fieldType, setFieldType] = useState<string>(props.dataTypes[0])



    return (
        <div className="horizontal-alignment">
            <div className="horizontal-alignment">
                <p>Field name:&nbsp;</p>
                <input type="text" value={fieldName} onChange={handleFieldNameEdit} />
            </div>
            <div className="horizontal-alignment">
                <p>Field type:&nbsp;</p>
                <select name="field-type" id="field-type" defaultValue={fieldType} onChange={handleFieldTypeEdit}>
                    {
                        props.dataTypes.map((dataType) => {
                            return <option key={dataType} value={dataType}>{dataType}</option>
                        })
                    }
                </select>
            </div>
            <div className="horizontal-alignment">
                <button onClick={() => { props.onFieldAddition(props.id) }}>+</button>
                <span>&nbsp;&nbsp;</span>
                {
                    props.showDelete &&
                    <button>delete</button>
                }
            </div>
        </div>
    )

    function handleFieldTypeEdit(event: React.ChangeEvent<HTMLSelectElement>) {
        props.onFieldUpdate(props.id, fieldName, event.target.value)
    }

    function handleFieldNameEdit(event: React.ChangeEvent<HTMLInputElement>) {
        setFieldName(event.target.value)
        props.onFieldUpdate(props.id, event.target.value, fieldType)
    }
}

export default FieldRowView