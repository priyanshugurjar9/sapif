import streamlit as st
import wikipedia

def verify_space_info(query):
    try:
        # Search Wikipedia
        wiki_results = wikipedia.search(query)
        wiki_page = wikipedia.page(wiki_results[0])
        wiki_content = wiki_page.content.lower()
        
        # Compare information and analyze
        response = {
            "query": query,
            "wikipedia_info": wiki_page.summary,
            "verified": True,
            "confidence_score": 0.0
        }
        
        # Simple verification logic
        keywords = query.lower().split()
        wiki_matches = sum(1 for keyword in keywords if keyword in wiki_content)
        confidence_score = (wiki_matches / len(keywords)) * 100
        
        response["confidence_score"] = confidence_score
        response["verified"] = confidence_score > 50
        
        return response
        
    except Exception as e:
        return {
            "error": str(e),
            "verified": False,
            "confidence_score": 0.0
        }

# Streamlit UI
st.set_page_config(
    page_title="Space Information Verifier",
    page_icon="🚀",
    layout="wide"
)

# Title and description
st.title("🚀 SPAIF")
st.markdown("""
This app verifies space-related information using Wikipedia data.
Enter your query about space or the universe to check its accuracy!
""")

# Input section
query = st.text_area("Enter your space-related query:", 
                     placeholder="Example: Mars is the fourth planet from the Sun",
                     height=100)

# Verify button
if st.button("Verify Information", type="primary"):
    if not query:
        st.error("Please enter a query to verify.")
    else:
        with st.spinner("Verifying information..."):
            result = verify_space_info(query)
            
            # Display results in columns
            if "no error" in result:
                st.error(f"An error occurred: {result['error']}")
            else:
                # Create three columns
                col1, col2 = st.columns(2)
                
                # Verification Status
                with col1:
                    st.metric(
                        "Verification Status",
                        "✅ Verified" if result["verified"] else "❌ Not Verified"
                    )
                
                # Confidence Score
                with col2:
                    st.metric(
                        "Confidence Score",
                        f"{result['confidence_score']:.1f}%"
                    )
                    st.progress(min(result["confidence_score"], 1.0))
                
                # Information sections
                st.subheader("Wikipedia Information")
                st.info(result["wikipedia_info"])

# Footer
st.markdown("---")
st.markdown("Wikipedia analysis")