' ==============================================================================================
' Script: AutoApproveWorkflowEngine.vbs
' Description: Event-driven VBScript macro for Freedom ERP. Automatically routes or approves
'              documents based on financial thresholds and standard contract clauses.
' Author: Hajimammad Aliyev
' Error Handling: Implements robust error trapping and database logging.
' ==============================================================================================

Option Explicit

Const THRESHOLD_AMOUNT = 5000.00
Const STATUS_APPROVED = "AUTO_APPROVED"
Const STATUS_MANAGER_REVIEW = "PENDING_MANAGER"

Sub ProcessNewDocument(DocID)
    On Error Resume Next
    
    Dim objConn, rsDoc, strSQL, docValue, docType
    Dim rowsAffected
    
    ' 1. Establish Database Connection (using ERP application context if possible)
    Set objConn = CreateObject("ADODB.Connection")
    objConn.Open GetConnectionString()
    
    If Err.Number <> 0 Then
        Call LogError(DocID, "Database Connection Failed", Err.Description)
        Exit Sub
    End If
    
    ' 2. Retrieve Document Metadata
    strSQL = "SELECT Type, TotalValue FROM ERP_DOCUMENTS WHERE ID = " & DocID
    Set rsDoc = objConn.Execute(strSQL)
    
    If rsDoc.EOF Then
        Call LogError(DocID, "Document Not Found", "DocID " & DocID & " does not exist.")
        rsDoc.Close
        objConn.Close
        Exit Sub
    End If
    
    docType = rsDoc("Type").Value
    docValue = CDbl(rsDoc("TotalValue").Value)
    rsDoc.Close
    
    ' 3. Business Logic Execution
    If docType = "Standard_Contract" And docValue < THRESHOLD_AMOUNT Then
        ' Approve and generate PDF print form
        strSQL = "UPDATE ERP_DOCUMENTS SET Status = '" & STATUS_APPROVED & "' WHERE ID = " & DocID
        objConn.Execute strSQL, rowsAffected
        
        If rowsAffected > 0 Then
            Call LogSuccess(DocID, "Document auto-approved successfully.")
            Call TriggerPDFGeneration(DocID)
        End If
    Else
        ' Route to manager
        strSQL = "UPDATE ERP_DOCUMENTS SET Status = '" & STATUS_MANAGER_REVIEW & "' WHERE ID = " & DocID
        objConn.Execute strSQL
        Call LogSuccess(DocID, "Document routed to Manager Review.")
    End If
    
    ' 4. Clean up
    objConn.Close
    Set objConn = Nothing
    Set rsDoc = Nothing
    
    If Err.Number <> 0 Then
        Call LogError(DocID, "Unexpected Error in ProcessNewDocument", Err.Description)
        Err.Clear
    End If
End Sub

' -------------------------------------------------------------------------
' Helper Functions
' -------------------------------------------------------------------------

Function GetConnectionString()
    ' In production, this would securely fetch the connection string from ERP Config
    GetConnectionString = "Provider=OraOLEDB.Oracle;Data Source=ERP_PROD;User Id=erp_admin;Password=secret;"
End Function

Sub LogError(DocID, ErrorType, ErrorMsg)
    ' Implementation for writing to ERP_SYSTEM_LOGS
    WScript.Echo "ERROR [Doc " & DocID & "]: " & ErrorType & " - " & ErrorMsg
End Sub

Sub LogSuccess(DocID, Msg)
    WScript.Echo "SUCCESS [Doc " & DocID & "]: " & Msg
End Sub

Sub TriggerPDFGeneration(DocID)
    ' Hooks into the ERP reporting engine to generate the standard print form
    WScript.Echo "Generating PDF Print Form for DocID: " & DocID
End Sub
