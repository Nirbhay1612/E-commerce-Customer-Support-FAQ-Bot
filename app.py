import streamlit as st
import time
import re

# Page Config
st.set_page_config(
    page_title="ShopEase Support",
    page_icon="🛍️",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ========== Bot Logic ==========
def get_bot_reply(user_msg: str) -> str:
    msg = user_msg.lower().strip()

    # Order Tracking
    if any(word in msg for word in ["track", "order status", "kahan hai", "kab aayega"]):
        return ("Order track karne ke liye mujhe **Order ID** chahiye.\n\n"
                "Format: `#ORD-XXXXXX`\n\n"
                "Example: `#ORD-784512`\n\n"
                "Order ID share karein, main exact status bataunga.")

    # Order ID detection
    if "ord-" in msg or "#ord" in msg or re.search(r"ord\d+", msg, re.IGNORECASE):
        digits = re.sub(r"\D", "", msg)
        last_digit = digits[-1] if digits else "0"

        if last_digit in ["1", "2"]:
            return ("Order mil gaya ✅\n\n"
                    "**Status:** Delivered\n"
                    "**Delivered on:** 18 September 2026\n\n"
                    "Agar product mein koi issue hai to 7 din ke andar return raise kar sakte ho.")
        elif last_digit in ["3", "4"]:
            return ("Order mil gaya ✅\n\n"
                    "**Status:** Out for Delivery\n"
                    "**Expected:** Aaj 8 PM tak deliver ho sakta hai\n"
                    "**Tracking:** TRK44556678\n\n"
                    "Delivery boy call karega delivery se pehle.")
        elif last_digit in ["5", "6"]:
            return ("Order mil gaya ✅\n\n"
                    "**Status:** Processing\n"
                    "**Expected Shipping:** 20 September 2026\n"
                    "**Expected Delivery:** 22-23 September 2026")
        else:
            return ("Order mil gaya ✅\n\n"
                    "**Status:** Shipped\n"
                    "**Tracking No:** TRK987654321\n"
                    "**Expected Delivery:** 21-22 September 2026")

    # Return
    if any(word in msg for word in ["return", "wapas", "refund"]):
        return ("**Return Policy:**\n\n"
                "✅ 7 days ke andar return allowed hai\n"
                "✅ Product unused + original packaging mein hona chahiye\n"
                "✅ Tags attached hone chahiye\n\n"
                "**Process:**\n"
                "1. Order ID batao\n"
                "2. Reason batao (Size / Defect / Wrong item)\n"
                "3. Main pickup schedule karwa dunga\n\n"
                "**Refund:** Pickup ke 5-7 working days baad original payment method mein.")

    # Exchange
    if any(word in msg for word in ["exchange", "badalna"]):
        return ("**Exchange Policy:**\n\n"
                "✅ Same product ke different size/color ke liye exchange allowed\n"
                "✅ 7 days ke andar request karni hogi\n"
                "✅ Product unused hona chahiye\n\n"
                "Order ID + kaunsa size/color chahiye wo batao.")

    # Delivery Delay
    if any(word in msg for word in ["delay", "late", "nahi aaya", "kitne din"]):
        return ("Delivery delay ke liye sincere apology 🙏\n\n"
                "**Normal delivery time:**\n"
                "• Metro cities: 2-4 days\n"
                "• Other cities: 4-7 days\n\n"
                "Exact status ke liye **Order ID** share karein.")

    # Promo
    if any(word in msg for word in ["promo", "coupon", "code", "discount"]):
        return ("**Promo Code Rules:**\n\n"
                "• Minimum order value: **₹1499**\n"
                "• Sirf selected categories pe apply hota hai\n"
                "• Ek user ek baar hi use kar sakta hai\n"
                "• Sale items pe additional discount nahi milta\n\n"
                "Kaunsa code try kar rahe ho aur cart amount kitna hai?")

    # Cancel
    if "cancel" in msg:
        return ("**Order Cancellation Policy:**\n\n"
                "✅ Processing stage mein hai to cancel ho sakta hai\n"
                "❌ Shipped ho chuka hai to cancel nahi hoga\n\n"
                "Cancel karne ke liye **Order ID** share karein.")

    # Payment
    if any(word in msg for word in ["payment", "pay", "fail", "transaction"]):
        return ("**Payment Help:**\n\n"
                "• Amount deduct ho gaya lekin order nahi bana → 3-5 working days mein auto refund\n"
                "• Payment failed → Dobara try karein\n\n"
                "Order ID ya Transaction ID share karein.")

    # Product
    if any(word in msg for word in ["product", "size", "chart", "material"]):
        return ("Product help ke liye specific product ka **name** ya **link** batao.\n\n"
                "Main size chart, material, care instructions etc. bata sakta hoon.")

    # Greetings
    if any(word in msg for word in ["hi", "hello", "namaste", "hey", "good morning", "good evening"]):
        return ("Namaste! 😊\n\n"
                "Main **ShopEase Support Assistant** hoon.\n"
                "Order tracking, return, exchange, payment ya kisi bhi issue mein madad kar sakta hoon.\n\n"
                "Batao kaise help karun?")

    # Thanks
    if any(word in msg for word in ["thank", "shukriya", "thanks", "ok", "okay"]):
        return "You're welcome! 😊\n\nAur kuch madad chahiye to bilkul batao. Happy shopping!"

    # Default
    return ("Samajh gaya. Main aapki madad karna chahta hoon.\n\n"
            "Thoda aur clear batao:\n"
            "• Order se related hai? → Order ID share karein\n"
            "• Return / Exchange chahiye?\n"
            "• Payment ya Promo code issue hai?")


# ========== Session State ==========
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": ("Namaste! 👋 Main **ShopEase Support Assistant** hoon.\n\n"
                        "Aapki kis cheez mein madad kar sakta hoon?\n"
                        "• Order tracking\n"
                        "• Returns & Refunds\n"
                        "• Product help\n"
                        "• Promo codes")
        }
    ]

# ========== Sidebar ==========
with st.sidebar:
    st.title("🛍️ ShopEase Support")
    st.markdown("---")
    
    if st.button("🗑️ Reset Conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": ("Namaste! 👋 Main **ShopEase Support Assistant** hoon.\n\n"
                            "Aapki kis cheez mein madad kar sakta hoon?\n"
                            "• Order tracking\n"
                            "• Returns & Refunds\n"
                            "• Product help\n"
                            "• Promo codes")
            }
        ]
        st.rerun()

    st.markdown("---")
    st.markdown("**Suggested Questions:**")
    
    suggestions = [
        "Mera order track karo",
        "Return karna hai",
        "Exchange chahiye",
        "Promo code issue",
        "Delivery delay ho gayi",
        "Payment fail ho gaya",
        "Cancel order karna hai"
    ]
    
    for suggestion in suggestions:
        if st.button(suggestion, use_container_width=True, key=suggestion):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            with st.spinner("Typing..."):
                time.sleep(0.6)
                reply = get_bot_reply(suggestion)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

# ========== Main Chat ==========
st.title("🛍️ ShopEase Support")
st.caption("Online • Usually replies instantly")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot reply
    with st.chat_message("assistant"):
        with st.spinner("Typing..."):
            time.sleep(0.7)
            reply = get_bot_reply(prompt)
            st.markdown(reply)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})