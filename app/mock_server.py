#!/usr/bin/env python3
# app/mock_server.py - minimal SOAP mock (GET ?wsdl and POST /mock)
from http.server import BaseHTTPRequestHandler, HTTPServer

WSDL = b"""<?xml version="1.0"?>
<definitions name="Mock" targetNamespace="http://example.com/soap"
  xmlns:tns="http://example.com/soap" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://schemas.xmlsoap.org/wsdl/">
  <types>
    <schema targetNamespace="http://example.com/soap" xmlns="http://www.w3.org/2001/XMLSchema">
      <element name="ProcessTransaction">
        <complexType>
          <sequence>
            <element name="recordId" type="string" minOccurs="0"/>
            <element name="name" type="string" minOccurs="0"/>
            <element name="amount" type="double" minOccurs="0"/>
            <element name="currency" type="string" minOccurs="0"/>
            <element name="timestamp" type="string" minOccurs="0"/>
            <element name="correlationId" type="string" minOccurs="0"/>
          </sequence>
        </complexType>
      </element>

      <element name="ProcessTransactionResponse">
        <complexType>
          <sequence>
            <element name="result" type="string" minOccurs="0"/>
          </sequence>
        </complexType>
      </element>
    </schema>
  </types>

  <message name="ProcessTransactionRequest"><part name="parameters" element="tns:ProcessTransaction"/></message>
  <message name="ProcessTransactionResponseMsg"><part name="parameters" element="tns:ProcessTransactionResponse"/></message>

  <portType name="MockPortType">
    <operation name="ProcessTransaction">
      <input message="tns:ProcessTransactionRequest"/>
      <output message="tns:ProcessTransactionResponseMsg"/>
    </operation>
  </portType>

  <binding name="MockBinding" type="tns:MockPortType">
    <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="ProcessTransaction">
      <soap:operation soapAction="ProcessTransaction" />
      <input><soap:body use="literal"/></input>
      <output><soap:body use="literal"/></output>
    </operation>
  </binding>

  <service name="MockService">
    <port name="MockPort" binding="tns:MockBinding">
      <soap:address location="http://localhost:8000/mock"/>
    </port>
  </service>
</definitions>
"""

RESPONSE = b"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ProcessTransactionResponse xmlns="http://example.com/soap">
      <result>SUCCESS</result>
    </ProcessTransactionResponse>
  </soap:Body>
</soap:Envelope>
"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), fmt%args))

    def do_GET(self):
        if self.path.endswith("?wsdl") or self.path.endswith("mock?wsdl"):
            self.send_response(200)
            self.send_header("Content-Type", "text/xml; charset=utf-8")
            self.send_header("Content-Length", str(len(WSDL)))
            self.end_headers()
            self.wfile.write(WSDL)
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length) if length else b""
        print("Received SOAP POST (len=%d) first100=%r" % (len(body), body[:100]))
        self.send_response(200)
        self.send_header("Content-Type", "text/xml; charset=utf-8")
        self.send_header("Content-Length", str(len(RESPONSE)))
        self.end_headers()
        self.wfile.write(RESPONSE)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Mock SOAP server listening on http://0.0.0.0:8000/mock")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
