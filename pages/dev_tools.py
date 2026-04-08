import streamlit as st
import requests
import base64
from fpdf import FPDF
from PIL import Image
import io

st.title("Ticket Tailor API Tool")

ORDER_ID = st.text_input("Enter Order ID", key="order_id_ticket_creation")

if st.button("Fetch Ticket"):
    if ORDER_ID:
        url = f"https://api.tickettailor.com/v1/issued_tickets?order_id=or_{ORDER_ID}"
        
        TICKET_TAILOR_API = st.secrets["ticket_tailor"]["API_KEY"]
        
        # Basic auth requires "username:password" encoded in base64.
        # Ticket Tailor typically uses the API Key as the username with no password.
        auth_str = f"{TICKET_TAILOR_API}:"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()
        
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded_auth}'
        }

        try:
            response = requests.request("GET", url, headers=headers)
            
            if response.status_code == 200:
                st.toast("Successfully fetched ticket data!")
                data = response.json()
                
                # Check if data exists and is a list of tickets
                tickets = data.get('data', [])
                if not tickets:
                    st.toast("No tickets found for this Order ID.")
                else:
                    pdf = FPDF()
                    
                    ticket = tickets[0] # replace with for ticket in tickets
                    QR_CODE_URL = ticket.get('qr_code_url')
                    BARCODE_URL = ticket.get('barcode_url')
                    TICKET_CODE = ticket.get('barcode')
                    TICKET_TYPE = ticket.get('description')
                    
                    if QR_CODE_URL and BARCODE_URL:
                        # 1. DOWNLOAD THE QR CODE AND BARCODE IMAGES
                        qr_img_response = requests.get(QR_CODE_URL)
                        barcode_img_response = requests.get(BARCODE_URL)
                        
                        if qr_img_response.status_code == 200 and barcode_img_response.status_code == 200:
                            qr_img_data = io.BytesIO(qr_img_response.content)
                            
                            # 2. TRANSFORM THE BARCODE IMAGE
                            barcode_img = Image.open(io.BytesIO(barcode_img_response.content))
                            barcode_img_rotated = barcode_img.rotate(-90, expand=True) # Rotate 90 deg clockwise (which is -90 deg)
                            barcode_img_data = io.BytesIO()
                            barcode_img_rotated.save(barcode_img_data, format='PNG')
                            barcode_img_data.seek(0)
                            
                            # 3. PDF CREATION LOGIC
                            pdf.add_page()
                            pdf.set_draw_color(5, 31, 170) # Set border color (RGB)
                            pdf.set_line_width(2.5) # Set border thickness
                            pdf.rect(5, 5, 200, 287) # Draw border: x, y, width, height
                            
                            # Add PDF Title
                            pdf.set_font("Helvetica", 'B', 22)
                            pdf.cell(text="VOICE OF GRACE - 2026", align='C') # PDF Heading
                            
                            # Add CODE Images
                            pdf.image(qr_img_data, x=10, y=25, w=120) # QR code on left
                            pdf.image(barcode_img_data, x=130, y=35, w=60) # Rotated barcode on right
                            
                            # Add TICKET CODE text and value
                            pdf.set_xy(12, 160)
                            pdf.set_font("Helvetica", '', 32)
                            pdf.cell(text="TICKET CODE", align='L')
                            pdf.set_xy(12, 170)
                            pdf.set_font("Helvetica", 'B', 70)
                            pdf.cell(text=str(TICKET_CODE), align='L')

                            # ADD TICKET TYPE text and value
                            pdf.set_xy(12, 200)
                            pdf.set_font("Helvetica", '', 32)
                            pdf.cell(text="TICKET TYPE", align='L')
                            pdf.set_xy(12, 210)
                            pdf.set_font("Helvetica", 'B', 40)
                            pdf.cell(text=str(TICKET_TYPE), align='L')

                        else:
                            st.error(f"Could not download the QR Code and Barcode images: {TICKET_CODE}!")
                    
                    # Generate PDF output
                    VOG_TICKETS_PDF = pdf.output()
                    
                    # Ensure it is bytes
                    if isinstance(VOG_TICKETS_PDF, str):
                        VOG_TICKETS_PDF = VOG_TICKETS_PDF.encode('latin-1')
                    elif isinstance(VOG_TICKETS_PDF, bytearray):
                        VOG_TICKETS_PDF = bytes(VOG_TICKETS_PDF)
                    
                    st.download_button(
                        label="Download Ticket PDF",
                        data=VOG_TICKETS_PDF,
                        file_name=f"VOG_TICKETS_{ORDER_ID}.pdf",
                        mime="application/pdf"
                    )

            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter an Order ID.")
