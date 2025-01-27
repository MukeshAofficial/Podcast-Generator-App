"use client";

import { useState } from 'react';
import axios from 'axios';
import { Loader2, Mic, Volume2, Link, File, X } from 'lucide-react';

const Home = () => {
    const [topic, setTopic] = useState('');
    const [url, setUrl] = useState('');
    const [podcastTitle, setPodcastTitle] = useState('');
    const [uploadedFile, setUploadedFile] = useState(null);
    const [podcastData, setPodcastData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('topic');


    const handleTopicSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setPodcastData(null);
        setError(null);
        try {
            const response = await axios.post('https://podcast-generator-app.onrender.com/generate_podcast_topic', { topic });
            setPodcastData(response.data);
        } catch (err) {
            setError(err.message || err.response?.data?.detail || "An unexpected error occurred!");
        } finally {
            setLoading(false);
        }
    };

    const handleUrlSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setPodcastData(null);
        setError(null);
        try {
            const response = await axios.post('https://podcast-generator-app.onrender.com/generate_podcast_url', { url, podcast_title: podcastTitle });
            setPodcastData(response.data);
        } catch (err) {
             setError(err.message || err.response?.data?.detail || "An unexpected error occurred!");
        } finally {
            setLoading(false);
        }
    };

  const handleDocumentSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setPodcastData(null);
        setError(null);
        try {
            const formData = new FormData();
            formData.append("uploaded_file", uploadedFile);
            formData.append("podcast_title", podcastTitle);


            const response = await axios.post('https://podcast-generator-app.onrender.com/generate_podcast_document', formData, {
                headers: {
                   'Content-Type': 'multipart/form-data',
                },
           });

            setPodcastData(response.data);
        } catch (err) {
            setError(err.message || err.response?.data?.detail || "An unexpected error occurred!");

        } finally {
            setLoading(false);
        }
    };



    const handleFileChange = (e) => {
        setUploadedFile(e.target.files[0]);
    };
    const clearFile = () => {
      setUploadedFile(null);
    }


    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto">
                <div className="bg-white rounded-xl shadow-xl p-6 space-y-8 transition-all duration-300 hover:shadow-2xl">
                    <div className="text-center space-y-4">
                        <Mic className="w-12 h-12 mx-auto text-blue-500 animate-pulse" />
                        <h1 className="text-3xl font-bold text-gray-800 tracking-tight">
                            AI Podcast Generator
                        </h1>
                        <p className="text-gray-600">Transform any topic, URL, or document into an engaging podcast</p>
                    </div>
                    <div className="flex space-x-4 border-b border-gray-200 mb-4">
                     <button
                       onClick={() => setActiveTab('topic')}
                       className={`py-2 px-4 rounded-t-lg transition-colors duration-200 font-medium text-gray-800 ${activeTab === 'topic' ? 'bg-blue-100 text-blue-700 border-b-2 border-blue-500' : 'hover:bg-gray-100'}`}
                     >
                        Topic
                      </button>
                      <button
                          onClick={() => setActiveTab('url')}
                          className={`py-2 px-4 rounded-t-lg transition-colors duration-200 font-medium text-gray-800 ${activeTab === 'url' ? 'bg-blue-100 text-blue-700 border-b-2 border-blue-500' : 'hover:bg-gray-100'}`}
                      >
                       URL
                      </button>
                      <button
                          onClick={() => setActiveTab('document')}
                          className={`py-2 px-4 rounded-t-lg transition-colors duration-200 font-medium text-gray-800 ${activeTab === 'document' ? 'bg-blue-100 text-blue-700 border-b-2 border-blue-500' : 'hover:bg-gray-100'}`}
                      >
                        Document
                      </button>
                  </div>
                 {activeTab === 'topic' && (
                   <form onSubmit={handleTopicSubmit} className="space-y-4">
                      <div className="relative">
                         <input
                            type="text"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            placeholder="Enter your podcast topic..."
                            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200 bg-gray-50 hover:bg-white"
                        />
                      </div>
                      <button
                          type="submit"
                          disabled={loading || !topic}
                          className={`w-full py-3 px-4 rounded-lg font-medium text-white transition-all duration-200 flex items-center justify-center space-x-2
                             ${loading || !topic
                             ? 'bg-gray-400 cursor-not-allowed'
                             : 'bg-blue-500 hover:bg-blue-600 active:transform active:scale-95'}`}
                      >
                            {loading ? (
                              <>
                                 <Loader2 className="w-5 h-5 animate-spin" />
                                 <span>Generating Podcast...</span>
                             </>
                              ) : (
                              <>
                                   <Mic className="w-5 h-5" />
                                   <span>Generate Podcast</span>
                               </>
                              )}
                        </button>
                    </form>
                 )}
                 {activeTab === 'url' && (
                    <form onSubmit={handleUrlSubmit} className="space-y-4">
                      <div className="relative">
                        <input
                           type="text"
                           value={podcastTitle}
                           onChange={(e) => setPodcastTitle(e.target.value)}
                           placeholder="Enter podcast title..."
                           className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200 bg-gray-50 hover:bg-white mb-2"
                        />
                         <input
                             type="text"
                             value={url}
                             onChange={(e) => setUrl(e.target.value)}
                             placeholder="Enter URL to scrape..."
                            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200 bg-gray-50 hover:bg-white"
                         />
                      </div>
                     <button
                          type="submit"
                          disabled={loading || !url}
                            className={`w-full py-3 px-4 rounded-lg font-medium text-white transition-all duration-200 flex items-center justify-center space-x-2
                             ${loading || !url
                             ? 'bg-gray-400 cursor-not-allowed'
                             : 'bg-blue-500 hover:bg-blue-600 active:transform active:scale-95'}`}
                      >
                            {loading ? (
                              <>
                                 <Loader2 className="w-5 h-5 animate-spin" />
                                 <span>Generating Podcast...</span>
                            </>
                           ) : (
                             <>
                                   <Link className="w-5 h-5" />
                                    <span>Generate Podcast</span>
                                </>
                              )}
                        </button>
                    </form>
                 )}
                   {activeTab === 'document' && (
                      <form onSubmit={handleDocumentSubmit} className="space-y-4" encType="multipart/form-data">
                           <div className="relative">
                             <input
                                type="text"
                                value={podcastTitle}
                                onChange={(e) => setPodcastTitle(e.target.value)}
                                placeholder="Enter podcast title..."
                                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200 bg-gray-50 hover:bg-white mb-2"
                              />
                             <div className="relative">
                              <input
                                  type="file"
                                  onChange={handleFileChange}
                                  id="upload-file"
                                 className="hidden"
                              />
                              <div className="flex items-center">
                                <label
                                  htmlFor="upload-file"
                                 className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200 bg-gray-50 hover:bg-white cursor-pointer flex items-center justify-between"
                               >
                                   {uploadedFile ?  <div className='flex items-center'>
                                        <File className="w-4 h-4 mr-2"/>
                                       <p className='truncate'>{uploadedFile.name}</p>
                                    </div>  : 'Upload a document'}
                                   {uploadedFile && <button type="button" onClick={clearFile} className="text-gray-500 hover:text-gray-700 focus:outline-none"><X className='w-4 h-4'/></button>}
                                </label>


                               </div>
                            </div>


                            </div>
                            <button
                            type="submit"
                                disabled={loading || !uploadedFile}
                            className={`w-full py-3 px-4 rounded-lg font-medium text-white transition-all duration-200 flex items-center justify-center space-x-2
                                  ${loading || !uploadedFile
                                 ? 'bg-gray-400 cursor-not-allowed'
                                 : 'bg-blue-500 hover:bg-blue-600 active:transform active:scale-95'}`}
                           >
                                {loading ? (
                                   <>
                                       <Loader2 className="w-5 h-5 animate-spin" />
                                       <span>Generating Podcast...</span>
                                   </>
                                ) : (
                                   <>
                                      <File className="w-5 h-5" />
                                      <span>Generate Podcast</span>
                                   </>
                               )}
                             </button>
                        </form>
                     )}



                    {error && (
                        <div className="p-4 rounded-lg bg-red-50 text-red-600 animate-fadeIn">
                            <p>Error: {error}</p>
                        </div>
                    )}

                    {podcastData && (
                        <div className="space-y-6 animate-fadeIn">
                            <div className="p-6 rounded-lg bg-gray-50 border border-gray-200">
                                <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
                                    <Volume2 className="w-5 h-5 mr-2 text-blue-500" />
                                    Generated Transcript
                                </h2>
                                <div className="prose prose-blue max-w-none">
                                    {podcastData.conversation.split('\n').map((paragraph, index) => (
                                        <p key={index} className="text-gray-700 mb-4">
                                            {paragraph}
                                        </p>
                                    ))}
                                </div>
                            </div>

                            {podcastData.audio_url && (
                                <div className="p-6 rounded-lg bg-blue-50 border border-blue-200">
                                    <h2 className="text-xl font-semibold text-gray-800 mb-4">
                                        Listen to Audio
                                    </h2>
                                    <audio
                                        controls
                                        src={podcastData.audio_url}
                                        className="w-full"
                                    >
                                        Your browser does not support the audio element.
                                    </audio>
                                </div>
                            )}

                            {podcastData.error && (
                                <div className="p-4 rounded-lg bg-red-50 text-red-600">
                                    <p>Audio Error: {podcastData.error}</p>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Home;
